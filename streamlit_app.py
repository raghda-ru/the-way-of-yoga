import streamlit as st
from pose.Pose import PoseDetector
from pose.stats import *
import cv2
import imutils
import time

st.set_page_config(page_title="The Way of Yoga", page_icon="🧘‍♀️")

# Add camera permissions
if 'camera' not in st.session_state:
    st.session_state.camera = st.camera_input("Enable camera")

# Add caching for heavy computations
@st.cache_resource
def load_pose_detector():
    return PoseDetector()

def main():
    st.title("The Way of Yoga")
    
    # Initialize pose detector
    detect = load_pose_detector()
    
    # Sidebar for pose selection
    pose_option = st.sidebar.selectbox(
        'Select Yoga Pose',
        ['Warrior I', 'Warrior II', 'Tree Pose']  # Add your poses here
    )
    
    # Video capture
    cap = cv2.VideoCapture(0)
    
    # Streamlit video frame
    frame_placeholder = st.empty()
    
    # Stop button
    stop = st.button('Stop')
    
    while not stop:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access webcam")
            break
            
        frame = imutils.resize(frame, width=1280)
        
        # Pose detection
        frame = detect.findPose(frame)
        positions = detect.findPosition(frame)
        
        if len(positions) != 0:
            # Get the appropriate position data based on selection
            position = warrior  # Replace with your position logic
            
            temps = []
            for angles in position:
                frame, temp = detect.calculate_angle(frame, positions, *angles)
                temps.append(temp)
        
        # Convert BGR to RGB for streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame
        frame_placeholder.image(frame, channels="RGB")
    
    cap.release()

if __name__ == '__main__':
    main() 