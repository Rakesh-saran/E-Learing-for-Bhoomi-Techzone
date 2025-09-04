from database.__init_db import (
    users_collection, courses_collection, lessons_collection, 
    enrollments_collection, payments_collection, reviews_collection,
    notifications_collection, quizzes_collection
)
from bson import ObjectId
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta, timezone
import pymongo

class AdminRepository:
    
    # Dashboard Statistics
    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        stats = {}
        
        # User statistics
        stats['total_users'] = users_collection.count_documents({})
        stats['active_users'] = users_collection.count_documents({"is_active": True})
        stats['inactive_users'] = users_collection.count_documents({"is_active": False})
        
        # Course statistics
        stats['total_courses'] = courses_collection.count_documents({})
        stats['published_courses'] = courses_collection.count_documents({"is_active": True})
        stats['unpublished_courses'] = courses_collection.count_documents({"is_active": False})
        
        # Enrollment statistics
        stats['total_enrollments'] = enrollments_collection.count_documents({})
        
        # Payment statistics
        payment_pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        payment_result = list(payments_collection.aggregate(payment_pipeline))
        stats['total_payments'] = payment_result[0]['total'] if payment_result else 0
        
        # Recent activity (last 7 days)
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        stats['new_users_this_week'] = users_collection.count_documents({
            "created_at": {"$gte": week_ago}
        }) if users_collection.find_one({"created_at": {"$exists": True}}) else 0
        
        stats['new_courses_this_week'] = courses_collection.count_documents({
            "created_at": {"$gte": week_ago}
        }) if courses_collection.find_one({"created_at": {"$exists": True}}) else 0
        
        return stats
    
    # Advanced User Management
    @staticmethod
    def get_users_with_stats(skip: int = 0, limit: int = 20, search: str = None, 
                           role_filter: str = None, active_filter: bool = None) -> List[Dict]:
        """Get users with enrollment and activity statistics"""
        pipeline = []
        
        # Match stage
        match_conditions = {}
        if search:
            match_conditions["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}}
            ]
        if role_filter:
            match_conditions["role"] = role_filter
        if active_filter is not None:
            match_conditions["is_active"] = active_filter
            
        if match_conditions:
            pipeline.append({"$match": match_conditions})
        
        # Lookup enrollments
        pipeline.extend([
            {
                "$lookup": {
                    "from": "enrollments",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "enrollments"
                }
            },
            {
                "$addFields": {
                    "total_enrollments": {"$size": "$enrollments"},
                    "id": {"$toString": "$_id"}
                }
            },
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "name": 1,
                    "email": 1,
                    "role": 1,
                    "is_active": 1,
                    "created_at": 1,
                    "last_login": 1,
                    "total_enrollments": 1
                }
            }
        ])
        
        return list(users_collection.aggregate(pipeline))
    
    @staticmethod
    def get_courses_with_stats(skip: int = 0, limit: int = 20, search: str = None,
                             active_filter: bool = None) -> List[Dict]:
        """Get courses with enrollment and lesson statistics"""
        pipeline = []
        
        # Match stage
        match_conditions = {}
        if search:
            match_conditions["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]
        if active_filter is not None:
            match_conditions["is_active"] = active_filter
            
        if match_conditions:
            pipeline.append({"$match": match_conditions})
        
        pipeline.extend([
            # Lookup instructor info
            {
                "$lookup": {
                    "from": "users",
                    "localField": "instructor_id",
                    "foreignField": "_id",
                    "as": "instructor"
                }
            },
            # Lookup enrollments
            {
                "$lookup": {
                    "from": "enrollments",
                    "localField": "_id",
                    "foreignField": "course_id",
                    "as": "enrollments"
                }
            },
            {
                "$addFields": {
                    "id": {"$toString": "$_id"},
                    "instructor_name": {"$arrayElemAt": ["$instructor.name", 0]},
                    "total_lessons": {"$size": "$lessons"},
                    "total_enrollments": {"$size": "$enrollments"}
                }
            },
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "title": 1,
                    "description": 1,
                    "instructor_id": {"$toString": "$instructor_id"},
                    "instructor_name": 1,
                    "total_lessons": 1,
                    "total_enrollments": 1,
                    "price": 1,
                    "is_active": 1,
                    "created_at": 1
                }
            }
        ])
        
        return list(courses_collection.aggregate(pipeline))
    
    # User CRUD Operations
    @staticmethod
    def create_user(user_data: Dict) -> str:
        """Create a new user"""
        user_data["created_at"] = datetime.now(timezone.utc)
        result = users_collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_user(user_id: str, update_data: Dict) -> bool:
        """Update user information"""
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Delete a user (soft delete by setting is_active to False)"""
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": False, "deleted_at": datetime.now(timezone.utc)}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def hard_delete_user(user_id: str) -> bool:
        """Permanently delete a user"""
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    # Course CRUD Operations
    @staticmethod
    def create_course(course_data: Dict) -> str:
        """Create a new course"""
        course_data["created_at"] = datetime.now(timezone.utc)
        if "instructor_id" in course_data:
            course_data["instructor_id"] = ObjectId(course_data["instructor_id"])
        result = courses_collection.insert_one(course_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_course(course_id: str, update_data: Dict) -> bool:
        """Update course information"""
        update_data["updated_at"] = datetime.now(timezone.utc)
        if "instructor_id" in update_data:
            update_data["instructor_id"] = ObjectId(update_data["instructor_id"])
        result = courses_collection.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_course(course_id: str) -> bool:
        """Delete a course (soft delete)"""
        result = courses_collection.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": {"is_active": False, "deleted_at": datetime.now(timezone.utc)}}
        )
        return result.modified_count > 0
    
    # Bulk Operations
    @staticmethod
    def bulk_user_action(user_ids: List[str], action: str) -> int:
        """Perform bulk actions on users"""
        object_ids = [ObjectId(uid) for uid in user_ids]
        
        if action == "activate":
            result = users_collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": True, "updated_at": datetime.now(timezone.utc)}}
            )
        elif action == "deactivate":
            result = users_collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}}
            )
        elif action == "delete":
            result = users_collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": False, "deleted_at": datetime.now(timezone.utc)}}
            )
        else:
            return 0
            
        return result.modified_count
    
    @staticmethod
    def bulk_course_action(course_ids: List[str], action: str) -> int:
        """Perform bulk actions on courses"""
        object_ids = [ObjectId(cid) for cid in course_ids]
        
        if action == "activate":
            result = courses_collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": True, "updated_at": datetime.now(timezone.utc)}}
            )
        elif action == "deactivate":
            result = courses_collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}}
            )
        elif action == "delete":
            result = courses_collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": False, "deleted_at": datetime.now(timezone.utc)}}
            )
        else:
            return 0
            
        return result.modified_count
    
    # Analytics and Reports
    @staticmethod
    def get_user_growth_analytics(days: int = 30) -> List[Dict]:
        """Get user growth analytics for the last N days"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "created_at": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$created_at"
                        }
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        return list(users_collection.aggregate(pipeline))
    
    @staticmethod
    def get_course_enrollment_analytics(days: int = 30) -> List[Dict]:
        """Get course enrollment analytics"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "enrolled_at": {"$gte": start_date}
                }
            },
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "course_id",
                    "foreignField": "_id",
                    "as": "course"
                }
            },
            {
                "$group": {
                    "_id": {
                        "course_id": "$course_id",
                        "course_title": {"$arrayElemAt": ["$course.title", 0]}
                    },
                    "enrollments": {"$sum": 1}
                }
            },
            {"$sort": {"enrollments": -1}},
            {"$limit": 10}
        ]
        
        return list(enrollments_collection.aggregate(pipeline))
    
    @staticmethod
    def get_instructor_performance() -> List[Dict]:
        """Get instructor performance statistics"""
        pipeline = [
            {
                "$match": {"role": "instructor"}
            },
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "_id",
                    "foreignField": "instructor_id",
                    "as": "courses"
                }
            },
            {
                "$lookup": {
                    "from": "enrollments",
                    "localField": "courses._id",
                    "foreignField": "course_id",
                    "as": "enrollments"
                }
            },
            {
                "$addFields": {
                    "total_courses": {"$size": "$courses"},
                    "total_enrollments": {"$size": "$enrollments"},
                    "active_courses": {
                        "$size": {
                            "$filter": {
                                "input": "$courses",
                                "cond": {"$eq": ["$$this.is_active", True]}
                            }
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "instructor_id": {"$toString": "$_id"},
                    "name": 1,
                    "email": 1,
                    "total_courses": 1,
                    "active_courses": 1,
                    "total_enrollments": 1
                }
            },
            {"$sort": {"total_enrollments": -1}}
        ]
        
        return list(users_collection.aggregate(pipeline))
