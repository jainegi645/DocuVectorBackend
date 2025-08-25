
# 
# and  [1.2,445343]


#Retrival - query fetch from vector db
# Augment - embedigs provided to llm. craft the response 
# Generation- spit our the response



def check_even_odd(number):
    if number%2 == 0:
        return {"result":"even"}
    else:
        return {"result":"odd"}
        
#     # Use an if statement to check if number is even
    
#     # Return a dictionary like {"result": "even"} or {"result": "odd"}
#     pass

# # Test it
print(check_even_odd(4))  # Should print {"result": "even"}
# print(check_even_odd(7))  # Should print {"result": "odd"}


# def divide_numbers(data):
#     try:
#         # data is a dictionary like {"a": 10, "b": 2}
#        return {"result": data['a'] / data['b']}
#     except ZeroDivisionError: 
#         return "error : Cannot divide by zero"

# # Test `it`
# print(divide_numbers({"a": 10, "b": 2}))  # Should print {"result": 5.0}
# print(divide_numbers({"a": 10, "b": 0}))  # Should print {"error": "Cannot divide by zero"}


# def square_numbers(numbers):
#     # Return a list of squares, e.g., [1, 4, 9] for [1, 2, 3]
#     return [num * num for num in numbers]

# # Test it
# print(square_numbers([1, 2, 3, 4]))  # Should print [1, 4, 9, 16]

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/great', methods=['POST'])
# def greet():
#    name =  request.json.get('name')
#    return jsonify({"message":f"hi {name}"})

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

class Person:
    def __init__(self, name):
       self.name = name
        
    def greet(self):
        return {"message": f" hi {self.name}"}
    
person = Person("jai")
print(person.greet())