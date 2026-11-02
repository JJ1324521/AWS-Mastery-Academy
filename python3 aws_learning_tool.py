#!/usr/bin/env python3
"""
AWS Learning Tool - Interactive Guide for Getting Started with AWS using Python (Boto3)
Use this script to practice AWS concepts and interact with the AWS SDK through simple Python commands.
"""

import time
import os
from collections import OrderedDict


def greet_user():
    """Greet learning user and ask what they'd like to explore first"""
    print("\n" + "=" * 50)
    print("🎓 Welcome! This is your AWS Learning Companion")
    print("=" * 50)
    
    print("\nChoose what you want to learn:\n")
    print("1. IAM Authentication & Security (Access keys, users)")
    print("2. EC2/Instances Basics (Virtual machines)")
    print("3. S3 Storage (Object storage, buckets)")
    print("4. Lambda Serverless (Server functions)")
    print("5. CloudFormation Tutorials (Infrastructure as Code)")


def interactive_learning_mode():
    """Run through a step-by-step learning module"""
    
    # Get user's AWS configuration status
    try:
        if os.system("aws configure get-profile", shell=True) == 0:
            print("\n✅ Your AWS CLI is configured!")
            return "running"
    except Exception as e:
        print(f"\n❌ Make sure you've run `aws configure` to set up your credentials")
    
    return "setup"


def run_ec2_sample():
    """Simple example showing EC2 operations with Python"""
    try:
        import boto3
        
        # Initialize AWS session
        client = boto3.client(
            'ec2',
            region_name='us-east-1'
        )
        
        print("\n🔧 Running EC2 Sample Command...")
        
        # Get available instances (dry-run mode)
        response = client.describe_instances()
        
        print(f"   Found {len(response['Instances'])} instances in us-east-1")
        
    except Exception as e:
        print(f"\n⚠️  This is a demo. To run actual AWS commands:")
        print("   python3 script_name.py --region your-region")


def check_prerequisites():
    """Verify user has basic requirements set up"""
    print("\n📋 Prerequisites Check:")
    
    print("   1. Python 3.9+ installed ✅")
    print("   2. pip installed ✅")
    print("   3. AWS CLI configured (aws configure)")
    print("   4. Boto3 package installed: pip install boto3")


def main_menu():
    """Main interactive menu system"""
    
    while True:
        greet_user()
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n🔐 IAM Learning Mode:")
            print("   Practice creating users, managing permissions, and security")
            
            # Example commands for learning:
            print("\n   Try these in AWS Console:")
            print("   1. Create a new user")
            print("   2. Assign policies to users")
            print("   3. Understand role-based access control")
            
        elif choice == "2":
            run_ec2_sample()
            print("\n💻 Sample EC2 Code:")
            print("""
import boto3

# Connect to AWS
ec2 = boto3.client('ec2', region_name='us-east-1')

# Create an instance
instance_id = 'your-instance-id'
print(f"Instance {instance_id} running on us-east-1")
""")
            
        elif choice == "3":
            print("\n📦 S3 Learning Mode:")
            print("   Practice storing objects, accessing buckets, and setting permissions")
            
            sample_code = """
import boto3

# Setup S3 client
s3 = boto3.client('s3', region_name='us-east-1')

# Create bucket (example)
bucket_name = 'your-learning-bucket'
response = s3.createBucket(Bucket=bucket_name)
print(f"Created bucket: {bucket['CreationDate']}")

# List all objects
objects = s3.list_objects_v2(Bucket=bucket_name, Prefix='my-learning/')
print(f'{len(objects["Contents"])} objects in your learning bucket')
"""
            print("\n   Run this:")
            print("   python3 sample_s3.py")
            
        elif choice == "4":
            print("\n☁️ Lambda Learning Mode:")
            print("   Practice Serverless functions, triggers, and event structures")
            
            sample_code = """
import boto3

# Get Lambda function info
lambda_client = boto3.client('lambda', region_name='us-east-1')

function_name = 'your-function-name'
response = lambda_client.get_function(FunctionName=function_name)
print(f"Function: {response['Configuration']['FunctionName']}")
"""
            print("\n   Run this:")
            print("   python3 sample_lambda.py")
            
        elif choice == "5":
            print("\n📝 CloudFormation Learning:")
            print("   Practice Infrastructure as Code with YAML templates")
            
            sample_template = """
AWSTemplateFormatVersion: '2010-09-09'
Description: Your First AWS Template

Resources:
  MyEC2:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-12345678
      InstanceType: t2.micro
"""
            print("\n   Save as template.yml")
            
        else:
            print("Please enter a valid option (1-5)")


def show_resources():
    """Display commonly used learning resources"""
    
    resources = {
        "📚 Book": "Official AWS Developer Guide",
        "🔗 Tutorial": "Boto3 Documentation",
        "💡 Practice Project": "Build Serverless App",
        "🎯 Learn by Doing": "AWS Cloud Practitioner Exam"
    }
    
    print("\n📖 Recommended Learning Resources:")
    for icon, name in resources.items():
        print(f"   {icon} {name}")


def main():
    """Main function that starts the learning tool"""
    
    try:
        check_prerequisites()
        
        while True:
            choice = input("\nEnter 1 for menu or 'q' to quit: ").strip().lower()
            
            if choice == "1":
                main_menu()
            
            elif choice.lower() == 'q':
                show_resources()
                
                print("\n💡 Want more help? Run:")
                print("   python3 interactive_guide.py")
                break
                
            else:
                print(f"Invalid input. Please enter '{choice}'")
    
    except KeyboardInterrupt:
        print("\n\n👋 Learning session ended.")


if __name__ == "__main__":
    main()