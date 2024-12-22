import pickle
import socket
import Cards
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_instructions(client_socket):
    
    while True:

        try:

            data = pickle.loads(client_socket.recv(2048))

            if data["type"] == "public_state":
                
                clear_console()
                
                print(f"Players: {data['player count']}")
                print("---------")
                print(f"data['turn']'s turn!")
                print("---------")
                
                for i in range(len(data["lower_hands"])):
                    print(f"Player {i+1}'s lower hand: {data['lower_hands'][i]}")
                    print("---------")

                print(f"Stack: {data['stack']}")


            elif data["type"] == "instruction":

                if data["action"] == "play_card":
                    print(f"Your hand: {data['hand']}")
                    card_index = int(input("Please input a card you would like to play: "))
                    response = {"action": "play_card", "index": card_index}
                    client_socket.send(pickle.dumps(response))

                elif data["action"] == "take_stack":
                    input("You cannot play any card. Press any key to take the entire stack.")
                    response = {"action": "take_stack"}
                    client_socket.send(pickle.dumps(response))

                elif data["action"] == "take_lower_card":
                    print(f"Your lower hand: {data['hand']}")
                    card_index = int(input("Please pick a card from your lower hand to play: "))
                    response = {"action": "play_lower_card", "index": card_index}
                    client_socket.send(pickle.dumps((response)))

                elif data["action"] == "play_hidden_card":
                    card_index = int(input(f"Please pick any out of your {len(data['hand'])} hidden cards to play: "))
                    response = {"action": "play_hidden_card", "index": card_index}
                    client_socket.send(pickle.dumps(response))

        except Exception as e:
            print(f"Error {e}")

def main():
    host= "192.168.1.38"
    port = 5050

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print("Connected!")
    
    except Exception as e:
        print(f"Failed connecting to {e}")

    handle_instructions(client_socket)


if __name__ == "__main__":
    main()