import cv2
import numpy as np
import pyrealsense2 as rs
import serial
import time

# ==== CONFIGURATION ====
ESP_PORT = 'COM6'              # Update to your actual COM port
BAUD_RATE = 115200
COLLISION_THRESHOLD = 0.2      # In meters
SAMPLE_RADIUS = 15
# ========================

# Global variables
measurement_point = None
distance_history = []
history_graph = np.zeros((200, 400, 3), dtype=np.uint8)

# Connect to ESP32
try:
    print(f"[INFO] Connecting to ESP32 on {ESP_PORT}...")
    esp = serial.Serial(ESP_PORT, BAUD_RATE)
    time.sleep(2)
except Exception as e:
    print(f"[ERROR] Could not connect to ESP32: {e}")
    esp = None

def mouse_callback(event, x, y, flags, param):
    global measurement_point
    if event == cv2.EVENT_LBUTTONDOWN and y >= 100:
        measurement_point = (x, y - 100)

def get_accurate_distance(depth_image, depth_scale, point, radius=15):
    x, y = point
    distances = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < depth_image.shape[1] and 0 <= ny < depth_image.shape[0]:
                dist_value = depth_image[ny, nx]
                if dist_value > 0:
                    distance = dist_value * depth_scale
                    if 0.1 <= distance <= 10.0:
                        distances.append(distance)
    return np.median(distances) if len(distances) > 5 else (np.mean(distances) if distances else 0)

def update_history_graph(distance):
    global history_graph
    history_graph[:, :-1] = history_graph[:, 1:]
    y_pos = int(history_graph.shape[0] * (1 - min(distance, 2.0) / 2.0))
    cv2.line(history_graph, (history_graph.shape[1] - 2, history_graph.shape[0] - 1),
             (history_graph.shape[1] - 1, y_pos), (0, 255, 0), 2)
    thresh_y = int(history_graph.shape[0] * (1 - COLLISION_THRESHOLD / 2.0))
    cv2.line(history_graph, (0, thresh_y), (history_graph.shape[1], thresh_y), (0, 0, 255), 1)
    cv2.putText(history_graph, f"{distance:.2f}m", (history_graph.shape[1]-80, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

def main():
    global measurement_point, distance_history, history_graph

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    align = rs.align(rs.stream.color)

    colorizer = rs.colorizer()
    colorizer.set_option(rs.option.color_scheme, 2)

    cv2.namedWindow("Collision Detection", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Collision Detection", mouse_callback)

    instructions = np.zeros((100, 640, 3), dtype=np.uint8)
    cv2.putText(instructions, "Click to measure | C: Center | R: Reset",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(instructions, f"COLLISION <= {COLLISION_THRESHOLD}m | ESC: Exit",
                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())
            display_image = np.vstack((instructions, depth_colormap))

            collision_detected = False
            current_distance = 0

            if measurement_point is not None:
                x, y = measurement_point
                current_distance = get_accurate_distance(depth_image, depth_scale, (x, y), SAMPLE_RADIUS)

                if current_distance > 0:
                    distance_history.append(current_distance)
                    if len(distance_history) > 10:
                        distance_history.pop(0)
                    update_history_graph(current_distance)

                    # Draw markers
                    cv2.circle(display_image, (x, y + 100), SAMPLE_RADIUS, (255, 255, 255), 1)
                    cv2.circle(display_image, (x, y + 100), 5, (0, 255, 255), -1)

                    if current_distance <= COLLISION_THRESHOLD:
                        collision_detected = True
                        if int(time.time() * 3) % 2 == 0:
                            cv2.rectangle(display_image, (0, 100), (display_image.shape[1], display_image.shape[0]),
                                          (0, 0, 255), 10)

                    color = (0, 255, 0) if current_distance > COLLISION_THRESHOLD * 1.5 else \
                            (0, 165, 255) if current_distance > COLLISION_THRESHOLD else (0, 0, 255)
                    text = f"Distance: {current_distance:.3f}m"
                    if collision_detected:
                        text += " - COLLISION!"
                    cv2.putText(display_image, text, (x - 100, y + 100 - 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Send signal to ESP32
            if esp:
                esp.write(b'1' if collision_detected else b'0')

            display_image[-history_graph.shape[0]:, :history_graph.shape[1]] = history_graph
            cv2.imshow("Collision Detection", display_image)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break
            elif key in [ord('r'), ord('R')]:
                distance_history.clear()
                history_graph.fill(40)
            elif key in [ord('c'), ord('C')]:
                measurement_point = (depth_image.shape[1] // 2, depth_image.shape[0] // 2)

    finally:
        pipeline.stop()
        if esp:
            esp.close()
        cv2.destroyAllWindows()
        print("[INFO] System shut down.")

if __name__ == "__main__":
    main()

