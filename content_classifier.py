import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import joblib  # For saving and loading the trained model

# Function to train the model and save it
def train_model():
    # Expanded dataset with more realistic examples
    data = pd.DataFrame({
        'subject': [
            "Urgent Payment Due", "Security Alert", "Account Verification", "Holiday Notice", 
            "Meeting Request", "Invoice Ready", "Password Reset Required", "Subscription Ending",
            "Job Application Update", "Interview Invitation", "Weekly Newsletter", "Special Offer",
            "Account Statement", "System Maintenance", "Data Analyst Position", "Job Opportunity",
            "Security Update Required", "Account Access", "Payment Confirmation", "Meeting Schedule",
            "Job Interview", "Career Opportunity", "Important Notice", "Action Required",
            "Urgent: Account Security", "Job Match Found", "Application Status"
        ],
        'content': [
            "Your payment is overdue", "Security breach detected", "Verify your account",
            "Office closure notice", "Team meeting tomorrow", "Invoice attached", 
            "Reset your password", "Renewal required", "Application received",
            "Interview scheduled", "Latest updates", "Limited time discount",
            "Monthly statement ready", "System downtime", "Job opening details",
            "Position available", "Update security settings", "Login attempt detected",
            "Payment processed", "Meeting confirmation", "Interview details",
            "Job opening at company", "Important update", "Action needed",
            "Security verification", "New job matches", "Application update"
        ],
        'is_essential': [
            1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1
        ]
    })

    # Combine subject and content
    data['text'] = data['subject'] + " " + data['content']

    X = data['text']
    y = data['is_essential']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Using a more sensitive model configuration
    model = make_pipeline(
        TfidfVectorizer(
            min_df=1,  # Changed from 2 to 1 to be more sensitive to unique terms
            max_features=1500,  # Increased from 1000
            stop_words='english'
        ),
        RandomForestClassifier(
            n_estimators=150,  # Increased from 100
            min_samples_split=2,  # Decreased from 5 to be more sensitive
            class_weight={0: 1, 1: 2},  # Weight essential emails more heavily
            random_state=42
        )
    )

    model.fit(X_train, y_train)
    joblib.dump(model, 'email_essential_model.pkl')

    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

# Function to classify whether an email is essential
def is_essential(content: str) -> bool:
    try:
        # Load the trained model
        model = joblib.load('email_essential_model.pkl')
        
        # Get prediction probability
        pred_prob = model.predict_proba([content])[0]
        prediction = pred_prob[1] >= 0.3  # Lower threshold to 0.3 (was implicitly 0.5)
        
        # Print detailed information
        print(f"Analyzing: {content[:100]}...")  # Show first 100 chars
        print(f"Confidence: {pred_prob[1]:.2%}")
        print(f"Classification: {'Essential' if prediction else 'Not essential'}\n")
        
        return prediction
    except Exception as e:
        print(f"Error in classification: {str(e)}")
        return True  # Default to treating as essential if there's an error

# Function to classify multiple emails (optional)
def classify_emails(emails: list):
    for email_content in emails:
        result = is_essential(email_content)
        print(f"Email: {email_content}\nIs essential: {'Yes' if result else 'No'}\n")

if __name__ == "__main__":
    # Uncomment this line to train the model when running the script
    train_model()

    # Example of classifying a new email
    new_email_content = "Your invoice is ready for payment"
    is_email_essential = is_essential(new_email_content)
    print(f"Is the email essential? {'Yes' if is_email_essential else 'No'}")

    # Example of classifying a list of emails
    emails = [
        "Action required: Your payment has failed.",
        "Happy holidays! Out of office till next week.",
        "Security alert: Account login attempt from new device.",
    ]
    classify_emails(emails)
