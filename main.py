import os
import time
from spot_controller import SpotController
import requests

ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']

# from supabase import create_client, Client

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)

def main():
    #example of using micro and speakers
    print("Start recording audio")
    sample_name = "aaaa.wav"
    cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    print(cmd)
    os.system(cmd)
    print("Playing sound")
    os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
    # Capture image
    import cv2
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    cv2.imwrite("img.png", image)
    camera_capture.release()
    
    # with open("img.png", 'rb') as f:
    #     supabase.storage.from_("testbucket").upload(file=f,path=path_on_supastorage)

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:

        for i in range(200):
            resp = requests.get("https://spot-rest-api.vercel.app/api/spot")
            command = resp.json()["message"]
            if command == "rest":
                time.sleep(3)
            if command == "forward":
                spot.move_to_goal(goal_x=0.1, goal_y=0)
            if command == "left":
                spot.move_by_velocity_control(v_x=0,v_y=0,v_rot=0.3,cmd_duration=5)
            if command == "right":
                spot.move_by_velocity_control(v_x=0,v_y=0,v_rot=-0.3,cmd_duration=5)
            time.sleep(1)
            
        
        # time.sleep(2)
        # spot.move_to_goal(goal_x=0.5, goal_y=0)
        # time.sleep(1)
        # spot.move_to_goal(goal_x=-0.5,goal_y=0)
        # time.sleep(1)
        # spot.move_by_velocity_control(v_x=0,v_y=0,v_rot=0.3,cmd_duration=5)
        # time.sleep(1)
        # spot.move_by_velocity_control(v_x=0,v_y=0,v_rot=-0.3,cmd_duration=5)
        # time.sleep(1)

        # # Move head to specified positions with intermediate time.sleep
        # spot.move_head_in_points(yaws=[0.2, 0],
        #                          pitches=[0.3, 0],
        #                          rolls=[0.4, 0],
        #                          sleep_after_point_reached=1)
        # time.sleep(3)

        # # Make Spot to move by goal_x meters forward and goal_y meters left
        # spot.move_to_goal(goal_x=0.5, goal_y=0)
        # time.sleep(3)

        # # Control Spot by velocity in m/s (or in rad/s for rotation)
        # spot.move_by_velocity_control(v_x=-0.3, v_y=0, v_rot=0, cmd_duration=2)
        # time.sleep(3)


if __name__ == '__main__':
    main()
