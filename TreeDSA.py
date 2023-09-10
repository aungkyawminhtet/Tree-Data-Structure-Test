# Aung Kyaw Min Htet
# Assigment VVII

import random
import pymongo


class Node:
    def __init__(self, data_list):
        self.data = data_list
        self.left = None
        self.right = None


class BTree:
    def __init__(self):
        self.connection = pymongo.MongoClient("localhost", 27017)
        self.database = self.connection["akmh"]
        self.collector = self.database["B_Tree"]

    def insert_data(self, new_data, node: Node):  # insert all data in Node
        # print(node.data)

        if node is None:
            node: Node = Node(new_data)
            return node

        if new_data["id"] < node.data["id"]:
            node.left = self.insert_data(new_data, node.left)

        if new_data["id"] > node.data["id"]:
            node.right = self.insert_data(new_data, node.right)

        return node

    def get_all_data(self, root_node):  # printing all data
        if root_node:
            self.get_all_data(root_node.left)
            print("All data is --> ", root_node.data)
            self.get_all_data(root_node.right)

    def b_search(self, new_node_data, root_node):  # to find data in b tree
        if root_node is None:
            # print("data is none")
            return False
        if new_node_data == root_node.data["email"] or new_node_data == root_node.data["password"]:
            # print("email is found")
            return True

        return self.b_search(new_node_data, root_node.left) or self.b_search(new_node_data, root_node.right)

    def search_data(self, new_search_data, root_node):  # to search one node data
        if root_node is None:
            # print("Node is empty")
            return False

        if new_search_data == root_node.data["email"]:
            data_list: list = []
            id = root_node.data["id"]
            email = root_node.data["email"]
            password = root_node.data["password"]
            name = root_node.data["name"]
            data_list: list = [id, email, password, name]
            return data_list
        return self.search_data(new_search_data, root_node.left) or self.search_data(new_search_data, root_node.right)

    def find_id(self, new_data, root_node):
        if root_node is None:
            return False

        if new_data == root_node.data["email"] or new_data == root_node.data["password"]:
            data_list: list = []
            f_id = root_node.data["id"]  # f_id = find id
            email = root_node.data["email"]
            password = root_node.data["password"]
            name = root_node.data["name"]
            data_list: list = [f_id, email, password, name]
            return data_list
        return self.find_id(new_data, root_node.left) or self.find_id(new_data, root_node.right)

    def del_fun_connector(self, new_del_data, root_node):
        id_list = self.find_id(new_del_data, root_node)

        if id_list:
            # print("connector data list => ", id_list)
            f_id = id_list[0]

            self.delete_node(f_id, root_node)
        else:
            print("Node data is not Found!")
            exit(1)

    def delete_node(self, f_id, root_node):
        if root_node is None:
            print("Node is empty Exit!")
            exit(1)
            # return root_node

        if f_id < root_node.data["id"]:
            root_node.left = self.delete_node(f_id, root_node.left)
        elif f_id > root_node.data["id"]:
            root_node.right = self.delete_node(f_id, root_node.right)
        else:
            if root_node.left is None:
                return root_node.right
            elif root_node.right is None:
                return root_node.left

            tem_data = self.find_min(root_node.right)
            root_node.data["id"] = tem_data.data["id"]

            root_node.right = self.delete_node(root_node.right, root_node.data["id"])

        return root_node

    def find_min(self, node):
        while node.left:
            node = node.left
        return node

    def update_data(self, root_node, new_data, target_data):
        if root_node is None:
            # print("Node is Empty")
            # exit(1)
            return
        if target_data == root_node.data["id"]:
            root_node.data["id"] = new_data

        elif target_data == root_node.data["email"]:
            root_node.data["email"] = new_data

        elif target_data == root_node.data["password"]:
            root_node.data["password"] = new_data

        elif target_data == root_node.data["name"]:
            root_node.data["name"] = new_data

        self.update_data(root_node.left, new_data, target_data)
        self.update_data(root_node.right, new_data, target_data)

    def all_data(self, root_node):
        d_id = random.randint(1, 1000)
        if root_node is not None:
            node_data = {
                "_id": d_id,
                "data": root_node.data,
                "left": self.all_data(root_node.left),
                "right": self.all_data(root_node.right)
            }

            self.collector.insert_one(node_data)

    def loading_data(self):
        data_list: dict = {}
        for i in self.collector.find({}, {"_id": 0, "data": 1}):
            # print("loading data is ", i["data"]["email"])
            d_id = len(data_list)
            all_data = {d_id: {"id": i["data"]["id"], "email": i["data"]["email"], "password": i["data"]["password"],
                               "name": i["data"]["name"]}}
            data_list.update(all_data)
        print("From loading function", data_list)
        return data_list


class Main:
    def __init__(self, main_node, main_b_tree):
        self.node = main_node
        self.b_tree = main_b_tree

    def mainHandler(self):
        user_input = input(
            "Press 1 to insert New Data\nPress 2 to get all data\nPress 3 to Search data\nPress 4 to search data list data\nPress 5 to Delete Node\nPress 6 to Update Node\nPress 7 to Store data in Db\nPress 8 to Exit Program :")
        if user_input == "1":
            self.insert_data()

        elif user_input == "2":
            self.getAllData()

        elif user_input == "3":
            self.find_data()

        elif user_input == "4":
            self.find_data_list()

        elif user_input == "5":
            self.delete_data()

        elif user_input == "6":
            self.update_data()

        elif user_input == "7":
            self.save_db()

        elif user_input == "8":
            exit(1)
        else:
            print("Invalid Option! Try Again!")
            self.mainHandler()

    def insert_data(self):
        print("###---This is insert section---###")
        email = input("Enter your email :")

        if self.b_tree.b_search(email, self.node):
            print("Email is Exit! Try Again!")
            self.insert_data()
        else:
            ram_id = random.randint(1, 20)
            password = input("Enter your password :")
            name = input("Enter your Name :")
            data_list = {"id": ram_id, "email": email, "password": password, "name": name}
            self.b_tree.insert_data(data_list, self.node)
            print("######################")
            print("---- Data is inserted ----")
            print("######################")
            self.mainHandler()

    def getAllData(self):
        print("###---This is get all data section---###")
        self.b_tree.get_all_data(self.node)
        # print("Exit program")
        self.mainHandler()

    def find_data(self):
        print("###---This is data search Section---###")
        user_data = input("Enter your search data(email,phone) :")
        response = self.b_tree.b_search(user_data, self.node)

        if response:
            print("###################################")
            print("Email or Phone is Found in Node")
            print("###################################")
            self.mainHandler()
        else:
            print("###################################")
            print("Email or Phone is not Found in Node")
            print("###################################")
            self.mainHandler()

    def find_data_list(self):
        print("###---This is data list find Section---###")
        user_data = input("Enter your search data list(email,phone) :")
        data_list = self.b_tree.search_data(user_data, self.node)
        if data_list:
            print("Data list is ==> ", data_list)
            self.mainHandler()
        else:
            print("Data list is not Exit in BST")
            self.find_data_list()

    def update_data(self):
        print("###---This is update data Section---###")
        user_data = input("Enter your Update data(email) :")
        data_list = self.b_tree.search_data(user_data, self.node)
        print("Update Node data list =>", data_list)
        d_data = input("Which data want to update :")
        u_data = input("Enter your update data :")
        self.b_tree.update_data(self.node, u_data, d_data)
        print("##################")
        print("Node data is updated")
        print("######################")
        self.mainHandler()

    def delete_data(self):
        print("###---This is Delete Node Section---###")
        del_user = input("Enter your Delete Node :")
        self.b_tree.del_fun_connector(del_user, self.node)
        print("########################")
        print("Node is Deleted")
        print("########################")
        self.mainHandler()

    def save_db(self):
        self.b_tree.all_data(self.node)
        print("########################")
        print("Data in Saved in DB")
        print("########################")
        self.mainHandler()


if __name__ == '__main__':
    b_tree = BTree()
    b_tree.loading_data()

    print("###---Please Enter Root Node Data---###")
    id: int = int(input("Enter Root Node id :"))
    email = input("Enter Root Node Email :")
    password = input("Enter Root Node password :")
    name = input("Enter Root Node Name :")
    data: dict = {"id": id, "email": email, "password": password, "name": name}

    node = Node(data)
    main_program = Main(node, b_tree)
    main_program.mainHandler()
