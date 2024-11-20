
import cv2
import time
import subprocess
import socket
import RPi.GPIO as GPIO
import smbus
import pygame
import pyttsx3
import chess
import chess.engine
from Adafruit_CharLCD import Adafruit_CharLCD
from picamera import PiCamera

# Initialize hardware
camera = PiCamera()
camera.resolution = (640, 480)
pygame.mixer.init()
engine = pyttsx3.init()
lcd = Adafruit_CharLCD()
lcd.clear()

# GPIO setup for servos
GPIO.setmode(GPIO.BCM)
servo_base, servo_shoulder, servo_elbow, servo_gripper = 17, 18, 19, 20
GPIO.setup(servo_base, GPIO.OUT)
GPIO.setup(servo_shoulder, GPIO.OUT)
GPIO.setup(servo_elbow, GPIO.OUT)
GPIO.setup(servo_gripper, GPIO.OUT)

base_pwm = GPIO.PWM(servo_base, 50)
shoulder_pwm = GPIO.PWM(servo_shoulder, 50)
elbow_pwm = GPIO.PWM(servo_elbow, 50)
gripper_pwm = GPIO.PWM(servo_gripper, 50)
base_pwm.start(7.5)
shoulder_pwm.start(7.5)
elbow_pwm.start(7.5)
gripper_pwm.start(7.5)

LCD_ADDR = 0x27
bus = smbus.SMBus(1)

# Stockfish path
STOCKFISH_PATH = "/usr/games/stockfish"

# Functions
def evaluate_move_with_stockfish(board, move_uci):
    stockfish_engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    move = chess.Move.from_uci(move_uci)
    board.push(move)
    info = stockfish_engine.analyse(board, chess.engine.Limit(time=2.0))
    evaluation_score = info['score'].relative.score(mate_score=10000)
    stockfish_engine.quit()
    if evaluation_score >= 200:
        return "Brilliant move!"
    elif evaluation_score >= 100:
        return "Great move!"
    elif evaluation_score >= 50:
        return "Good move!"
    elif evaluation_score >= -50:
        return "Inaccurate move."
    elif evaluation_score >= -100:
        return "Mistake."
    elif evaluation_score >= -200:
        return "Blunder!"
    else:
        return "Very poor move."

def chess_to_arm_coords(square):
    square_size = 30
    origin_x, origin_y = 100, 100
    z_pick, z_place = 20, 0
    file, rank = square[0], int(square[1])
    file_index = ord(file) - ord('a')
    rank_index = rank - 1
    x = origin_x + file_index * square_size
    y = origin_y + rank_index * square_size
    z = z_pick
    return {"x": x, "y": y, "z": z}

def move_servo(pwm, angle):
    duty_cycle = 2.5 + (angle / 18)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)

def pick_and_place(start_coords, end_coords):
    move_servo(base_pwm, start_coords['x'])
    move_servo(shoulder_pwm, start_coords['y'])
    move_servo(elbow_pwm, start_coords['z'])
    move_servo(gripper_pwm, 45)
    move_servo(base_pwm, end_coords['x'])
    move_servo(shoulder_pwm, end_coords['y'])
    move_servo(elbow_pwm, end_coords['z'])
    move_servo(gripper_pwm, 90)

def display_on_lcd(message):
    lcd.clear()
    lcd.message(message)
    time.sleep(2)

def speak_message(message):
    engine.say(message)
    engine.runAndWait()

def receive_from_raspberry1():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024).decode()
    client_socket.close()
    move, evaluation_message = data.split(',')
    return move, evaluation_message

def main():
    board = chess.Board()
    while True:
        move, evaluation_message = receive_from_raspberry1()
        start_square, end_square = move[:2], move[2:]
        move_obj = chess.Move.from_uci(move)
        if move_obj in board.legal_moves:
            board.push(move_obj)
            display_on_lcd(f"Move: {move}\n{evaluation_message}")
            speak_message(f"Move: {move}. {evaluation_message}")
            start_coords = chess_to_arm_coords(start_square)
            end_coords = chess_to_arm_coords(end_square)
            pick_and_place(start_coords, end_coords)
            best_move = evaluate_move_with_stockfish(board, move)
            display_on_lcd(f"Best move: {best_move}")
            speak_message(f"Best move: {best_move}")

if __name__ == "__main__":
    main()
