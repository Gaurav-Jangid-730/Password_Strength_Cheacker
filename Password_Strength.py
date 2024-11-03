import re

# Function to load common passwords into a set for fast lookup
def load_common_passwords(filename):
    common_passwords_set = set()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_password = line.strip().lower()  # Normalize to lowercase
                if cleaned_password:  # Only add non-empty entries
                    common_passwords_set.add(cleaned_password)

        print("Common passwords loaded successfully.")
        print(f"Total number of common passwords loaded: {len(common_passwords_set)}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please make sure it exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return common_passwords_set

# Load common passwords from the file into a set
common_passwords = load_common_passwords("common_passwords.txt")

# Password strength checking functions
def check_basic_criteria(password):
    score = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("The password is too short. It should be at least 8 characters long.")

    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("The password must contain at least one lowercase letter (a-z).")

    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("The password must contain at least one uppercase letter (A-Z).")

    # Check for digits
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("The password must contain at least one digit (0-9).")

    # Check for special characters
    if re.search(r"[!@#$%^&*()_+=-]", password):
        score += 1
    else:
        feedback.append("The password must contain at least one special character (e.g., !@#$%^&*).")

    # Additional checks for patterns
    if re.search(r"(.)\1{2,}", password):  # e.g., "aaa" or "111"
        feedback.append("The password contains repeated characters (e.g., 'aaa' or '111'), which is not secure.")
    if re.search(r"(abc|123|qwerty|password|iloveyou)", password.lower()):
        feedback.append("The password contains common patterns or sequences (e.g., 'abc', '123', 'password') which can be easily guessed.")

    return score, feedback

def check_password_strength(password):
    # Normalize the password input to lowercase
    normalized_password = password.lower()
    
    # First, check basic criteria (length, character types, patterns)
    score, feedback = check_basic_criteria(password)

    # Check if the password is in the common passwords set
    if normalized_password in common_passwords:
        feedback.append("The password is too common and may be easily guessed. Consider using a more unique password.")
        return "Very Weak", feedback

    # Determine strength based on score
    if score <= 2:
        return "Weak", feedback
    elif score == 3 or score == 4:
        return "Moderate", feedback
    else:
        return "Strong", feedback


# Test the function
password = input("Enter a password to check its strength: ")
strength, feedback = check_password_strength(password)
print(f"The password strength is: {strength}")
if feedback:
    print("Feedback:")
    for message in feedback:
        print(f"- {message}")
