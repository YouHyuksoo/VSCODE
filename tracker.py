import math
import time

class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.last_detected_time = {}  # 각 객체의 마지막 감지 시간 저장


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        current_time = time.time()  # 현재 시간
        
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 100:
                    self.center_points[id] = (cx, cy) # print(self.center_points)
                    self.last_detected_time[id] = current_time  # 시간 업데이트

                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                self.last_detected_time[self.id_count] = current_time  # 새 객체 시간 저장
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        new_last_detected_time = {}
        
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
            new_last_detected_time[object_id] = self.last_detected_time[object_id]

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        self.last_detected_time = new_last_detected_time.copy()
        return objects_bbs_ids