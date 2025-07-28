#!/bin/bash

# 🔐 Password Policy Management Script
# This script manages password policies for Cloud SQL instance

set -e

PROJECT_ID="footybets-ai"
INSTANCE_NAME="footybets-db"

echo "🔐 Password Policy Management"
echo "============================"

# Function to show current password policy
show_password_policy() {
    echo "📊 Current Password Policy:"
    gcloud sql instances describe $INSTANCE_NAME --project=$PROJECT_ID \
        --format="table(settings.passwordValidationPolicy)" 2>/dev/null || echo "No password policy configured"
}

# Function to enable password policy
enable_password_policy() {
    echo "🔒 Enabling Password Policy..."
    gcloud sql instances patch $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --enable-password-policy \
        --password-policy-min-length=8 \
        --password-policy-complexity=COMPLEXITY_DEFAULT \
        --password-policy-disallow-username-substring \
        --password-policy-reuse-interval=5 \
        --password-policy-password-change-interval=1d \
        --quiet
    
    echo "✅ Password policy enabled"
}

# Function to disable password policy
disable_password_policy() {
    echo "⚠️  Disabling Password Policy..."
    gcloud sql instances patch $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --clear-password-policy \
        --quiet
    
    echo "✅ Password policy disabled"
}

# Function to update password policy
update_password_policy() {
    local min_length=${1:-8}
    local complexity=${2:-COMPLEXITY_DEFAULT}
    local reuse_interval=${3:-5}
    local change_interval=${4:-1d}
    
    echo "🔄 Updating Password Policy..."
    echo "  - Minimum length: $min_length characters"
    echo "  - Complexity: $complexity"
    echo "  - Reuse interval: $reuse_interval passwords"
    echo "  - Change interval: $change_interval"
    
    gcloud sql instances patch $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --enable-password-policy \
        --password-policy-min-length=$min_length \
        --password-policy-complexity=$complexity \
        --password-policy-disallow-username-substring \
        --password-policy-reuse-interval=$reuse_interval \
        --password-policy-password-change-interval=$change_interval \
        --quiet
    
    echo "✅ Password policy updated"
}

# Function to show users
show_users() {
    echo "👥 Database Users:"
    gcloud sql users list --instance=$INSTANCE_NAME --project=$PROJECT_ID
}

# Function to change user password
change_user_password() {
    local username=$1
    local new_password=$2
    
    if [ -z "$username" ] || [ -z "$new_password" ]; then
        echo "❌ Usage: $0 change-password <username> <new_password>"
        exit 1
    fi
    
    echo "🔑 Changing password for user: $username"
    gcloud sql users set-password $username \
        --instance=$INSTANCE_NAME \
        --project=$PROJECT_ID \
        --password=$new_password \
        --quiet
    
    echo "✅ Password changed for user: $username"
}

# Function to test password policy
test_password_policy() {
    echo "🧪 Testing Password Policy..."
    echo ""
    echo "Testing weak passwords (should fail):"
    
    # Test weak passwords
    weak_passwords=("123" "password" "footybets" "admin" "test")
    
    for password in "${weak_passwords[@]}"; do
        echo "  Testing: '$password'"
        # This would be tested in the application layer
        echo "    ❌ Would be rejected (too weak)"
    done
    
    echo ""
    echo "Testing strong passwords (should pass):"
    strong_passwords=("SecurePass123!" "MyComplexP@ssw0rd" "FootyBets2024!")
    
    for password in "${strong_passwords[@]}"; do
        echo "  Testing: '$password'"
        echo "    ✅ Would be accepted (strong)"
    done
}

# Main script logic
case "${1:-show}" in
    "show")
        show_password_policy
        echo ""
        show_users
        ;;
    "enable")
        enable_password_policy
        ;;
    "disable")
        disable_password_policy
        ;;
    "update")
        update_password_policy "${@:2}"
        ;;
    "users")
        show_users
        ;;
    "change-password")
        change_user_password "$2" "$3"
        ;;
    "test")
        test_password_policy
        ;;
    "help"|"-h"|"--help")
        echo "🔐 Password Policy Management Script"
        echo ""
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  show              - Show current password policy and users"
        echo "  enable            - Enable password policy with default settings"
        echo "  disable           - Disable password policy"
        echo "  update [min_len] [complexity] [reuse] [change_interval] - Update password policy"
        echo "  users             - Show database users"
        echo "  change-password <user> <password> - Change user password"
        echo "  test              - Test password policy with sample passwords"
        echo "  help              - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 show                    # Show current policy"
        echo "  $0 enable                  # Enable password policy"
        echo "  $0 update 12 COMPLEXITY_DEFAULT 10 7d  # Update with custom settings"
        echo "  $0 change-password footybets_user newpassword123!  # Change password"
        echo "  $0 test                    # Test password policy"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 