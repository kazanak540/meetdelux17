#!/usr/bin/env python3
"""
Add multiple images to hotels and rooms
"""

import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meetdelux')

# Additional hotel images (3-5 per hotel)
ADDITIONAL_HOTEL_IMAGES = [
    # Hotel 1 - Grand Horizon
    ["https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800", 
     "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800",
     "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800"],
    
    # Hotel 2 - Aegean
    ["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800",
     "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800",
     "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800"],
    
    # Hotel 3 - Anatolian
    ["https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800",
     "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800",
     "https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?w=800"],
    
    # Hotel 4 - Mediterranean
    ["https://images.unsplash.com/photo-1573052905904-34ad8c27f0cc?w=800",
     "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800",
     "https://images.unsplash.com/photo-1602002418082-a4443e081dd1?w=800"],
    
    # Hotel 5 - Black Sea
    ["https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800",
     "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
     "https://images.unsplash.com/photo-1590073242678-70ee3fc28e8e?w=800"],
]

# Additional room images
ADDITIONAL_ROOM_IMAGES = [
    ["https://images.unsplash.com/photo-1519167758481-83f29da8c851?w=800",
     "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800"],
    
    ["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800",
     "https://images.unsplash.com/photo-1587293852726-70cdb56c2866?w=800"],
    
    ["https://images.unsplash.com/photo-1572290292358-0ea8b6d79ec8?w=800",
     "https://images.unsplash.com/photo-1595436069962-24c6c1e27e78?w=800"],
]


async def main():
    print("="*60)
    print("📸 Adding Multiple Images to Hotels & Rooms")
    print("="*60)
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Get all hotels
        hotels = await db.hotels.find().to_list(length=100)
        print(f"\n🏨 Found {len(hotels)} hotels")
        
        # Add images to first 5 hotels
        for i, hotel in enumerate(hotels[:5]):
            if i < len(ADDITIONAL_HOTEL_IMAGES):
                additional_images = ADDITIONAL_HOTEL_IMAGES[i]
                
                # Get current images
                current_images = hotel.get('images', [])
                
                # Add new images
                all_images = current_images + additional_images
                
                await db.hotels.update_one(
                    {"id": hotel["id"]},
                    {"$set": {"images": all_images}}
                )
                
                print(f"   ✅ {hotel['name']}: {len(current_images)} → {len(all_images)} images")
        
        # Get all rooms
        rooms = await db.conference_rooms.find().to_list(length=100)
        print(f"\n🎯 Found {len(rooms)} rooms")
        
        # Add images to first 30 rooms
        for i, room in enumerate(rooms[:30]):
            room_images_set = ADDITIONAL_ROOM_IMAGES[i % len(ADDITIONAL_ROOM_IMAGES)]
            
            # Get current images
            current_images = room.get('images', [])
            
            # Add new images
            all_images = current_images + room_images_set
            
            await db.conference_rooms.update_one(
                {"id": room["id"]},
                {"$set": {"images": all_images}}
            )
            
            if i < 5:  # Print first 5
                print(f"   ✅ {room['name']}: {len(current_images)} → {len(all_images)} images")
        
        if len(rooms) > 5:
            print(f"   ✅ ... and {min(25, len(rooms)-5)} more rooms updated")
        
        print("\n" + "="*60)
        print("✅ IMAGES ADDED SUCCESSFULLY!")
        print("="*60)
        print(f"📸 Hotels updated: 5")
        print(f"📸 Rooms updated: {min(30, len(rooms))}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
