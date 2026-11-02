#!/usr/bin/env python3
"""
AWS Mastery Academy
A standalone Tkinter learning application for AWS beginners and aspiring
cloud / infrastructure technicians.

No third-party packages are required. Progress is saved locally as JSON.
"""

import json
import random
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

APP_NAME = "AWS Mastery Academy"
DATA_FILE = Path.home() / ".aws_mastery_academy_progress.json"

COLORS = {
    "navy": "#14213D",
    "navy2": "#1D3557",
    "blue": "#2878B5",
    "cyan": "#56B4D3",
    "orange": "#F4A261",
    "bg": "#F3F6FA",
    "white": "#FFFFFF",
    "text": "#172033",
    "muted": "#64748B",
    "green": "#238636",
    "red": "#C0392B",
    "border": "#DCE3EC",
}

LEARNING_PATH = [
    ("1", "Cloud fundamentals", "Understand cloud computing, shared responsibility, regions, Availability Zones and pricing."),
    ("2", "Core infrastructure", "Learn EC2, AMIs, instance types, EBS, snapshots, and basic Linux administration."),
    ("3", "Storage and backup", "Understand S3, EBS, EFS, storage classes, versioning, lifecycle rules and backups."),
    ("4", "Networking", "Learn VPCs, subnets, route tables, internet gateways, NAT, security groups and DNS."),
    ("5", "Identity and security", "Practise IAM users, groups, roles, policies, MFA, KMS and least privilege."),
    ("6", "Databases", "Compare RDS, Aurora and DynamoDB; learn backups, availability and database connectivity."),
    ("7", "Automation and serverless", "Explore Lambda, API Gateway, SQS, SNS, EventBridge and CloudFormation."),
    ("8", "Monitoring and operations", "Use CloudWatch, CloudTrail, AWS Config, Systems Manager and troubleshooting methods."),
    ("9", "Architecture and reliability", "Study Well-Architected principles, scaling, load balancing, resilience and disaster recovery."),
    ("10", "Portfolio and certification", "Build documented projects and prepare for the AWS Certified Cloud Practitioner exam."),
]

MODULES = [
    {
        "title": "Cloud Computing Fundamentals",
        "level": "Beginner",
        "summary": "Understand what cloud computing is and why organisations use AWS.",
        "topics": [
            ("What is cloud computing?", "Cloud computing provides on-demand access to computing resources such as servers, storage, databases and networking over the internet. Instead of buying and maintaining every physical server, a company can provision resources when needed."),
            ("IaaS, PaaS and SaaS", "IaaS provides building blocks such as virtual machines and networks. PaaS provides a managed platform for deploying applications. SaaS provides a finished application. EC2 is an IaaS example; a managed application platform is closer to PaaS; web-based email is SaaS."),
            ("Regions and Availability Zones", "An AWS Region is a separate geographic area. Each Region contains multiple isolated Availability Zones (AZs). Deploying across more than one AZ can improve availability if one AZ has a problem."),
            ("Shared Responsibility Model", "AWS is responsible for security OF the cloud, including the physical facilities and underlying infrastructure. Customers are responsible for security IN the cloud, such as IAM permissions, data protection, operating-system patching on EC2 and network rules. The exact split depends on the service."),
            ("Pay-as-you-go and cost control", "Many AWS services charge based on usage, storage, requests, data transfer or running time. Set a budget and billing alerts before experimenting. Free Tier eligibility and limits vary; not every resource or usage pattern is free."),
        ],
        "terms": "Region • Availability Zone • scalability • elasticity • IaaS • PaaS • SaaS • shared responsibility • pay-as-you-go",
        "practice": "Draw a simple diagram showing a user connecting to an application hosted in one Region across two Availability Zones. Label the web tier, database tier and network boundary.",
    },
    {
        "title": "Amazon EC2 and Compute",
        "level": "Beginner",
        "summary": "Learn how virtual servers work and how to operate them safely.",
        "topics": [
            ("What is EC2?", "Amazon Elastic Compute Cloud (EC2) provides resizable virtual servers called instances. You choose an Amazon Machine Image (AMI), instance family and size, storage, network and security settings."),
            ("AMI and instance types", "An AMI is a template used to launch an instance, often containing an operating system and initial software. Instance families are optimised for different workloads, such as general purpose, compute, memory or storage."),
            ("Key pairs and access", "A key pair is commonly used for secure SSH access to Linux instances. Keep private keys private. Never upload them to GitHub, email them to others or include them in screenshots."),
            ("EBS volumes and snapshots", "Elastic Block Store (EBS) provides persistent block storage for EC2. Snapshots are point-in-time backups. Plan backup retention and test restoration rather than assuming a backup is usable."),
            ("Operations and troubleshooting", "Check instance state, system status checks, security groups, subnet route tables, public IP settings, operating-system firewall and service logs. A running instance does not automatically mean the application is healthy."),
        ],
        "terms": "EC2 • AMI • instance type • EBS • snapshot • key pair • user data • security group • status checks",
        "practice": "Create a diagram of a small EC2 deployment. Identify the AMI, instance, EBS volume, subnet, security group and how an administrator would connect.",
    },
    {
        "title": "Amazon S3 and Storage",
        "level": "Beginner",
        "summary": "Understand object storage, file storage and block storage.",
        "topics": [
            ("What is S3?", "Amazon Simple Storage Service (S3) is object storage. Data is stored as objects inside buckets. Objects have keys, metadata and content. S3 is commonly used for backups, logs, static website assets and data lakes."),
            ("Buckets, objects and keys", "A bucket is a container for objects. An object key identifies an object within the bucket. Bucket names are globally unique within the S3 partition and should not contain sensitive information."),
            ("Storage classes", "S3 offers storage classes for different access patterns, including frequently accessed data, infrequent access and archival data. Lower storage cost can come with retrieval charges or delays, so choose based on recovery requirements."),
            ("Security and public access", "Keep Block Public Access enabled unless you have a carefully reviewed reason otherwise. Use IAM and bucket policies to grant only required access. Do not put credentials or private customer data in a public bucket."),
            ("Versioning and lifecycle", "Versioning can preserve previous object versions after overwrites or deletes. Lifecycle rules can transition or expire objects. Versioning is useful but does not replace a complete backup and recovery plan."),
        ],
        "terms": "S3 • bucket • object • key • bucket policy • versioning • lifecycle rule • storage class • encryption",
        "practice": "Design a secure backup bucket: private access, versioning, encryption, a lifecycle policy and a documented restore test.",
    },
    {
        "title": "VPC and Cloud Networking",
        "level": "Beginner",
        "summary": "Build the networking knowledge needed for cloud infrastructure support.",
        "topics": [
            ("What is a VPC?", "A Virtual Private Cloud (VPC) is a logically isolated network in AWS. You select an IPv4 CIDR range and place resources in subnets. Plan address space carefully to avoid overlap with office networks or VPN-connected sites."),
            ("Public and private subnets", "A subnet is public when its route table has a route to an internet gateway. A private subnet does not have a direct route to an internet gateway. A public IP alone does not make a resource reachable; routing and security controls must also allow it."),
            ("Route tables and gateways", "Route tables decide where network traffic goes. An internet gateway enables internet connectivity for eligible VPC resources. A NAT gateway allows resources in private subnets to initiate outbound IPv4 internet connections without accepting unsolicited inbound connections."),
            ("Security groups and network ACLs", "Security groups are stateful virtual firewalls attached to network interfaces. Network ACLs are stateless subnet-level filters. Start with restrictive rules and allow only the ports and sources required."),
            ("DNS and connectivity checks", "Route 53 provides DNS services. Troubleshoot in layers: name resolution, route, security rules, host firewall, listening service and application health. Tools such as nslookup, ping, traceroute and curl can help, but some networks block ICMP."),
        ],
        "terms": "VPC • CIDR • subnet • route table • internet gateway • NAT gateway • security group • NACL • DNS",
        "practice": "Draw a VPC with two Availability Zones, a public subnet and private subnet in each AZ, an internet gateway and a NAT gateway. Explain the route for each tier.",
    },
    {
        "title": "IAM and Cloud Security",
        "level": "Beginner",
        "summary": "Learn how AWS identities, permissions and security controls work.",
        "topics": [
            ("What is IAM?", "Identity and Access Management (IAM) controls who can access AWS resources and what actions they can perform. IAM policies are JSON documents that define permissions."),
            ("Users, groups and roles", "Users represent identities, groups organise users, and roles provide temporary credentials to trusted principals. Workloads should generally use roles instead of long-lived access keys."),
            ("Least privilege", "Grant only the actions and resources required. Avoid using broad administrator permissions for everyday work. Review permissions regularly and remove unused access."),
            ("MFA and root user", "Enable multi-factor authentication on the account root user and protect its credentials. Avoid using the root user for routine tasks. Create an administrative identity with appropriate controls."),
            ("Encryption and audit", "AWS Key Management Service (KMS) helps create and manage encryption keys. CloudTrail records account activity and API events. CloudWatch provides metrics, logs and alarms for operational monitoring."),
        ],
        "terms": "IAM • policy • principal • role • least privilege • MFA • KMS • CloudTrail • encryption",
        "practice": "Write down a policy design for a developer who only needs to read objects from one specific S3 bucket. Explain why wildcard permissions are risky.",
    },
    {
        "title": "AWS Databases",
        "level": "Intermediate",
        "summary": "Choose the right database and understand reliability basics.",
        "topics": [
            ("Relational databases and RDS", "Amazon RDS is a managed relational database service supporting engines such as PostgreSQL and MySQL. It handles many routine administration tasks, but customers still need to plan access, schema, backups and performance."),
            ("Aurora", "Amazon Aurora is a relational database compatible with MySQL and PostgreSQL. It is designed for cloud operation and offers managed storage and availability capabilities."),
            ("DynamoDB", "Amazon DynamoDB is a managed NoSQL key-value and document database. It is useful for predictable low-latency access patterns and can scale without managing database servers."),
            ("Backups and Multi-AZ", "Automated backups and snapshots support recovery. Multi-AZ deployments improve availability but are not a substitute for backups. Define recovery point and recovery time objectives."),
            ("Choosing a database", "Use relational databases when relationships, SQL and transactions are central. Consider DynamoDB for key-based access patterns at scale. Model the workload before selecting a service."),
        ],
        "terms": "RDS • Aurora • DynamoDB • SQL • NoSQL • Multi-AZ • snapshot • backup • RPO • RTO",
        "practice": "Choose a database for an online store, explain your choice, and identify the data that should be backed up and how recovery would be tested.",
    },
    {
        "title": "Serverless and Application Integration",
        "level": "Intermediate",
        "summary": "Build event-driven applications without managing servers.",
        "topics": [
            ("AWS Lambda", "Lambda runs code in response to events without requiring you to manage servers. You configure a runtime, handler, memory, timeout and permissions. You are still responsible for code quality, security and monitoring."),
            ("API Gateway", "API Gateway can expose HTTP or REST APIs and route requests to backend services such as Lambda. Authentication, throttling, validation and logging are important design considerations."),
            ("SQS and SNS", "Simple Queue Service (SQS) decouples application components using queues. Simple Notification Service (SNS) distributes messages to subscribers. Queues help absorb spikes and support retry patterns."),
            ("EventBridge", "Amazon EventBridge routes events between applications and AWS services using rules. It is useful for scheduled jobs and event-driven automation."),
            ("Failure handling", "Design for retries, duplicate messages, timeouts and dead-letter queues. A successful event trigger does not guarantee the business operation completed; monitor outcomes and errors."),
        ],
        "terms": "Lambda • API Gateway • SQS • SNS • EventBridge • event-driven • dead-letter queue • retry",
        "practice": "Sketch an order-processing flow: API Gateway receives an order, Lambda validates it, SQS queues work and a worker processes it.",
    },
    {
        "title": "Monitoring, Operations and Troubleshooting",
        "level": "Intermediate",
        "summary": "Use logs, metrics and audit trails to investigate incidents.",
        "topics": [
            ("CloudWatch", "CloudWatch collects metrics and logs, provides dashboards and can trigger alarms. Monitor both infrastructure and application indicators, such as CPU, latency, error rate and disk utilisation."),
            ("CloudTrail", "CloudTrail records AWS account activity and API calls. It helps answer who performed an action, when it happened and which resources were affected."),
            ("AWS Systems Manager", "Systems Manager helps manage and operate AWS resources, including automation, inventory and session access. Use approved roles and access controls."),
            ("Troubleshooting method", "Define the impact, start time and scope. Check recent changes, health dashboards, logs, network paths, permissions and resource status. Change one thing at a time and record the result."),
            ("Incident documentation", "Record symptoms, affected users/resources, timestamps, evidence, actions taken, results, escalation details and next steps. Avoid placing passwords, secret keys or unnecessary personal data in tickets."),
        ],
        "terms": "CloudWatch • CloudTrail • Systems Manager • metrics • logs • alarms • incident • root cause",
        "practice": "Write a mock incident report for an EC2 web server that is running but cannot be reached. Include checks, evidence, resolution and prevention.",
    },
    {
        "title": "High Availability, Scaling and Architecture",
        "level": "Advanced",
        "summary": "Understand how production systems remain available and recover from failures.",
        "topics": [
            ("Elastic Load Balancing", "A load balancer distributes incoming traffic across targets such as EC2 instances. Health checks help route traffic only to healthy targets."),
            ("Auto Scaling", "EC2 Auto Scaling adjusts the number of instances based on demand or schedules. Capacity planning, health checks and scaling policies help balance availability and cost."),
            ("Resilience across AZs", "Deploying across multiple Availability Zones reduces dependence on a single AZ. Consider what happens if an instance, subnet, AZ or Region becomes unavailable."),
            ("Backup and disaster recovery", "Define RPO (how much data loss is acceptable) and RTO (how quickly service must recover). Select backup, pilot-light, warm-standby or multi-site approaches based on business needs and cost."),
            ("Well-Architected thinking", "The AWS Well-Architected Framework considers operational excellence, security, reliability, performance efficiency, cost optimisation and sustainability. Use these pillars to review designs."),
        ],
        "terms": "ELB • Auto Scaling • health check • fault tolerance • resilience • RPO • RTO • Well-Architected",
        "practice": "Design a two-AZ web application and explain how it handles an instance failure, an AZ outage and a database recovery.",
    },
]

PROJECTS = [
    {
        "name": "Secure Static Website",
        "level": "Beginner",
        "time": "2–4 hours",
        "services": ["Amazon S3", "CloudFront (optional)", "IAM", "ACM (optional)"],
        "goal": "Publish a simple static HTML/CSS website while learning object storage and secure access.",
        "steps": [
            "Create a small HTML page locally with a title, short introduction and contact section (do not publish private details).",
            "Create an S3 bucket in a Region you choose. Keep Block Public Access enabled initially.",
            "Upload your website files and review object permissions and bucket settings.",
            "For a secure public website, consider CloudFront with a private S3 origin using Origin Access Control rather than making the bucket public.",
            "If using a custom domain, study Route 53 and an ACM certificate in the Region required by CloudFront.",
            "Test the site from a browser and document the architecture, security choices and estimated costs.",
        ],
        "success": "A working website, architecture diagram, screenshots with account details hidden, and a short explanation of how S3 and CloudFront work.",
        "cost": "Potential charges can apply for storage, requests, CloudFront, DNS and data transfer. Remove resources when finished and check billing.",
    },
    {
        "name": "EC2 Linux Web Server",
        "level": "Beginner",
        "time": "3–5 hours",
        "services": ["Amazon EC2", "EBS", "VPC", "Security Groups", "CloudWatch"],
        "goal": "Launch a Linux virtual server and host a basic web page.",
        "steps": [
            "Review EC2 pricing, instance types and the current Free Tier/Free Plan eligibility before launching anything.",
            "Launch a small test EC2 instance using an approved Amazon Linux AMI and a suitable key pair.",
            "Create a security group that allows SSH only from your own trusted public IP and HTTP only if required.",
            "Connect using SSH or EC2 Instance Connect where available. Never share your private key.",
            "Install a web server using the distribution's package manager and create a simple test page.",
            "Check the instance status checks, web service status, security group, route table and operating-system firewall if the page fails.",
            "Create a short runbook explaining how to stop, start, back up and safely terminate the instance.",
        ],
        "success": "A reachable test web page, a labelled network diagram and a troubleshooting runbook.",
        "cost": "EC2 compute, EBS storage, public IPv4 addresses and data transfer may incur charges. Stop or terminate resources when done; stopping does not remove every charge.",
    },
    {
        "name": "VPC Network Design Lab",
        "level": "Beginner–Intermediate",
        "time": "3–5 hours",
        "services": ["VPC", "Subnets", "Route Tables", "Internet Gateway", "NAT Gateway", "Security Groups"],
        "goal": "Design a segmented network similar to a small company environment.",
        "steps": [
            "Choose a private CIDR range that does not overlap with networks you may connect to.",
            "Create a VPC and two Availability Zones.",
            "Create public and private subnets in each Availability Zone.",
            "Attach an internet gateway and configure public-subnet routes.",
            "Study NAT gateway routing for private-subnet outbound access. Do not create a NAT gateway casually; it can have ongoing charges.",
            "Create restrictive security groups for a web tier and an application tier.",
            "Draw traffic flows and explain why a private instance is not directly reachable from the public internet.",
        ],
        "success": "A labelled VPC diagram, route-table explanation and security-group rule table.",
        "cost": "VPC components have different pricing. NAT gateways and public IPv4 addresses can cost money. You can complete much of this project as a diagram before deploying resources.",
    },
    {
        "name": "Cloud Monitoring and Alerts",
        "level": "Intermediate",
        "time": "2–4 hours",
        "services": ["CloudWatch", "EC2", "SNS", "CloudTrail"],
        "goal": "Monitor a test workload and create an alerting workflow.",
        "steps": [
            "Use a test EC2 instance or a sample metric so you understand what is being monitored.",
            "Open CloudWatch and explore available metrics and dashboards.",
            "Create an alarm for a suitable metric, such as CPU utilisation, with a clearly defined threshold.",
            "Optionally create an SNS topic and subscription for notifications; confirm subscription if required.",
            "Trigger a safe test condition and observe the alarm state transition.",
            "Review CloudTrail events to understand how account actions can be audited.",
            "Document what the alarm detects, what it does not detect and what an on-call technician should do next.",
        ],
        "success": "A dashboard or alarm, a notification test and a short monitoring runbook.",
        "cost": "CloudWatch metrics, alarms, logs and SNS usage may be billable. Review current pricing and remove test resources.",
    },
    {
        "name": "IAM Least-Privilege Lab",
        "level": "Intermediate",
        "time": "2–3 hours",
        "services": ["IAM", "S3", "CloudTrail"],
        "goal": "Practise access control by granting only the permissions a task requires.",
        "steps": [
            "Use a test account or sandbox and enable MFA for privileged identities.",
            "Create a private test S3 bucket with a harmless sample file.",
            "Create a test role or identity for a read-only task.",
            "Write a policy that allows only the required read actions on the specific bucket and objects.",
            "Test an allowed action and a denied action, then inspect the result.",
            "Review the policy for unnecessary wildcards and remove test access when finished.",
        ],
        "success": "A least-privilege policy, evidence of allowed and denied actions, and a short security explanation.",
        "cost": "IAM itself generally has no additional charge, but related services may. Never use production identities or real customer data for this lab.",
    },
    {
        "name": "Serverless Contact Form API",
        "level": "Intermediate",
        "time": "4–6 hours",
        "services": ["API Gateway", "Lambda", "DynamoDB", "IAM", "CloudWatch"],
        "goal": "Build a simple API that accepts and stores test form submissions.",
        "steps": [
            "Design a small JSON request with validation rules. Use fake test data only.",
            "Create a DynamoDB table with a suitable partition key.",
            "Create a Lambda function that validates the request and writes an item to DynamoDB.",
            "Give the Lambda execution role only the required DynamoDB permissions.",
            "Expose the function through an API Gateway endpoint.",
            "Test valid, invalid and missing-field requests.",
            "Review logs, error handling, throttling and how you would protect the API in production.",
        ],
        "success": "A working test endpoint, sample requests/responses, a simple architecture diagram and security notes.",
        "cost": "API Gateway, Lambda, DynamoDB and CloudWatch usage can be billable. Set budgets and delete test resources after the lab.",
    },
    {
        "name": "S3 Event-Driven File Processor",
        "level": "Advanced",
        "time": "5–8 hours",
        "services": ["S3", "Lambda", "SQS", "CloudWatch", "IAM"],
        "goal": "Process a file automatically after it is uploaded, with retry and failure handling.",
        "steps": [
            "Create separate private input and output buckets, or clearly separated prefixes.",
            "Create an SQS queue and understand visibility timeout and message retention.",
            "Create a Lambda function that reads a harmless test file and writes a processed result.",
            "Configure event routing so uploads trigger processing without creating a recursive trigger loop.",
            "Use a dead-letter queue or failure destination where appropriate.",
            "Add CloudWatch logs and an alarm for errors or a growing queue.",
            "Test duplicate events, invalid files and retry behaviour. Make processing idempotent.",
        ],
        "success": "A working event flow, failure-handling demonstration, diagram and operational notes.",
        "cost": "S3 requests/storage, Lambda, SQS and CloudWatch can incur charges. Clean up all resources and review the bill.",
    },
    {
        "name": "Highly Available Web Architecture",
        "level": "Advanced",
        "time": "6–10 hours",
        "services": ["VPC", "EC2", "Application Load Balancer", "Auto Scaling", "RDS", "CloudWatch"],
        "goal": "Design a production-style web application across multiple Availability Zones.",
        "steps": [
            "Start with an architecture diagram before creating resources.",
            "Place an Application Load Balancer in public subnets across two Availability Zones.",
            "Place application instances in private subnets and use an Auto Scaling group.",
            "Design a database tier with appropriate network isolation and backup strategy.",
            "Define health checks, scaling signals, monitoring and alert thresholds.",
            "Document how the system behaves if one instance or one Availability Zone becomes unavailable.",
            "Estimate monthly cost and compare a fully deployed lab with a diagram-only portfolio version.",
        ],
        "success": "A multi-AZ architecture diagram, availability explanation, cost estimate and incident runbook.",
        "cost": "This project can become expensive. Load balancers, NAT gateways, EC2, RDS, storage and data transfer can all incur charges. Build a diagram first and deploy only with a budget and cleanup plan.",
    },
]

QUESTIONS = [
    ("What does AWS stand for?", ["Amazon Web Services", "Advanced Web Software", "Amazon Wide Systems", "Automated Web Storage"], 0, "AWS stands for Amazon Web Services, the cloud platform provided by Amazon."),
    ("Which AWS service provides virtual servers?", ["Amazon S3", "Amazon EC2", "Amazon Route 53", "AWS IAM"], 1, "EC2 provides resizable virtual machine instances."),
    ("What type of storage is Amazon S3?", ["Block storage", "Object storage", "Relational storage", "Memory storage"], 1, "S3 stores data as objects inside buckets."),
    ("Which service runs code in response to events without managing servers?", ["AWS Lambda", "Amazon EBS", "Amazon VPC", "AWS Direct Connect"], 0, "Lambda is AWS's event-driven serverless compute service."),
    ("Which service is a managed NoSQL database?", ["Amazon RDS", "Amazon Redshift", "Amazon DynamoDB", "Amazon EFS"], 2, "DynamoDB is a managed key-value and document NoSQL database."),
    ("Which service provides managed relational databases?", ["Amazon RDS", "Amazon SQS", "Amazon CloudFront", "AWS IAM"], 0, "RDS manages supported relational database engines."),
    ("What does IAM control?", ["DNS records", "Identity and permissions", "Virtual machine CPU", "Object compression"], 1, "IAM controls identities and what actions they can perform."),
    ("What is an AWS Region?", ["A single EC2 server", "A geographic area containing multiple Availability Zones", "A security group", "A billing invoice"], 1, "A Region is a separate geographic area with multiple isolated AZs."),
    ("What is the main purpose of a security group?", ["Encrypt an EBS snapshot", "Act as a virtual firewall for resources", "Register a domain", "Create an S3 bucket"], 1, "Security groups control inbound and outbound traffic for associated network interfaces."),
    ("Which service provides DNS domain registration and routing?", ["Route 53", "CloudTrail", "ECS", "EBS"], 0, "Route 53 is AWS's DNS and domain registration service."),
    ("What does MFA add to sign-in?", ["A second verification factor", "More storage", "A public IP", "A faster CPU"], 0, "Multi-factor authentication requires another proof of identity."),
    ("Which service records AWS API activity for auditing?", ["CloudTrail", "CloudFront", "EFS", "Elastic Beanstalk"], 0, "CloudTrail records account activity and API events."),
    ("What is an EBS volume commonly used for?", ["Block storage attached to EC2", "Public DNS", "Email delivery", "Content delivery"], 0, "EBS provides block storage volumes for EC2 instances."),
    ("What does a VPC provide?", ["A logically isolated virtual network", "A managed email inbox", "A code editor", "A billing discount"], 0, "A VPC is your logically isolated network in AWS."),
    ("Which component determines where subnet traffic is routed?", ["Route table", "IAM group", "S3 key", "AMI"], 0, "Route tables contain routes that direct network traffic."),
    ("Which service distributes incoming application traffic across targets?", ["Elastic Load Balancing", "AWS Artifact", "Amazon S3 Glacier", "AWS Budgets"], 0, "Elastic Load Balancing distributes traffic across registered targets."),
    ("What is the purpose of an S3 lifecycle rule?", ["Automatically transition or expire objects", "Change EC2 passwords", "Create VPC subnets", "Assign IAM users"], 0, "Lifecycle rules automate object transitions and expiration."),
    ("Which service helps create alarms from metrics?", ["CloudWatch", "Route 53", "IAM", "KMS"], 0, "CloudWatch provides metrics, logs, dashboards and alarms."),
    ("What does least privilege mean?", ["Give everyone administrator access", "Grant only the permissions required", "Disable all logging", "Share one root account"], 1, "Least privilege reduces risk by limiting permissions to what is needed."),
    ("What is an Availability Zone?", ["An isolated location within an AWS Region", "A DNS record", "A type of IAM policy", "A storage class"], 0, "AZs are isolated locations within a Region, designed for fault isolation."),
    ("Which service provides managed message queues?", ["Amazon SQS", "Amazon EBS", "AWS KMS", "Amazon Route 53"], 0, "SQS is a managed message queuing service."),
    ("What does CloudFront provide?", ["Content delivery network", "Relational database", "Virtual private network", "Identity federation"], 0, "CloudFront caches and delivers content through edge locations."),
    ("What is an AMI used for?", ["A template to launch EC2 instances", "A DNS health check", "An S3 access log", "A database query"], 0, "An Amazon Machine Image contains the information needed to launch an EC2 instance."),
    ("What does RPO describe?", ["Maximum acceptable data loss measured in time", "CPU performance", "Network latency", "The number of IAM users"], 0, "Recovery Point Objective describes the maximum acceptable data loss."),
    ("What does RTO describe?", ["Target time to restore a service", "S3 object size", "A subnet mask", "A type of encryption key"], 0, "Recovery Time Objective is the target time to restore a service after disruption."),
    ("Which service manages encryption keys?", ["AWS KMS", "Amazon SNS", "Amazon ECS", "AWS Budgets"], 0, "KMS helps create and manage cryptographic keys."),
    ("What is the purpose of an SQS dead-letter queue?", ["Hold messages that repeatedly fail processing", "Store EC2 AMIs", "Host a website", "Resolve DNS"], 0, "A DLQ isolates messages that could not be processed successfully."),
    ("Which AWS service can run containers?", ["Amazon ECS", "Amazon Route 53", "Amazon S3", "AWS KMS"], 0, "ECS is a container orchestration service."),
    ("What is the shared responsibility model?", ["AWS and customer divide security responsibilities", "AWS handles every customer configuration", "Customers manage AWS data centres", "It is a pricing model"], 0, "AWS secures the cloud infrastructure; customers secure their workloads and configurations according to the service."),
    ("What should you do before experimenting with billable AWS resources?", ["Set a budget and understand pricing", "Share root credentials", "Disable MFA", "Make all resources public"], 0, "Understand current pricing, set budgets/alerts and clean up resources after labs."),
]

def load_progress():
    try:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"completed_modules": [], "completed_projects": [], "best_score": 0, "quizzes_taken": 0}

def save_progress(progress):
    try:
        DATA_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    except Exception as exc:
        messagebox.showwarning("Progress not saved", f"Could not save progress:\n{exc}")

class ScrollFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=COLORS["bg"])
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner.bind("<Configure>", self._configure)
        self.canvas.bind("<Configure>", self._resize)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._wheel)

    def _configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

class AWSMasteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1180x780")
        self.root.minsize(900, 620)
        self.root.configure(bg=COLORS["bg"])
        self.progress = load_progress()
        self.current_question = 0
        self.quiz_questions = []
        self.quiz_score = 0
        self.quiz_answer = tk.IntVar(value=-1)
        self.quiz_feedback = None
        self.module_lookup = {m["title"]: m for m in MODULES}
        self.project_lookup = {p["name"]: p for p in PROJECTS}
        self._style()
        self._layout()
        self.show_dashboard()

    def _style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 23, "bold"), foreground=COLORS["navy"])
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground=COLORS["muted"])
        style.configure("Card.TFrame", background=COLORS["white"], relief="flat")
        style.configure("CardTitle.TLabel", background=COLORS["white"], foreground=COLORS["navy"], font=("Segoe UI", 12, "bold"))
        style.configure("CardText.TLabel", background=COLORS["white"], foreground=COLORS["text"], font=("Segoe UI", 10))
        style.configure("Nav.TButton", font=("Segoe UI", 10), padding=(12, 10), anchor="w")
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
        style.configure("TCheckbutton", background=COLORS["white"], font=("Segoe UI", 10))
        style.configure("TRadiobutton", background=COLORS["white"], font=("Segoe UI", 10))

    def _layout(self):
        self.sidebar = tk.Frame(self.root, bg=COLORS["navy"], width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="AWS MASTERY", bg=COLORS["navy"], fg="white",
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=18, pady=(24, 2))
        tk.Label(self.sidebar, text="ACADEMY  |  LEARN • BUILD • GROW", bg=COLORS["navy"],
                 fg="#B9C7D8", font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=19, pady=(0, 24))
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Learning Roadmap", self.show_roadmap),
            ("AWS Learning Modules", self.show_modules),
            ("Project Challenges", self.show_projects),
            ("Knowledge Quiz", self.start_quiz),
            ("Career & Portfolio", self.show_career),
        ]
        for label, command in nav_items:
            ttk.Button(self.sidebar, text=label, command=command, style="Nav.TButton").pack(fill="x", padx=10, pady=3)
        tk.Frame(self.sidebar, bg="#344766", height=1).pack(fill="x", padx=16, pady=20)
        tk.Label(self.sidebar, text="YOUR GOAL", bg=COLORS["navy"], fg="#B9C7D8",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=19)
        tk.Label(self.sidebar, text="Build real cloud skills\none step at a time.", bg=COLORS["navy"],
                 fg="white", justify="left", font=("Segoe UI", 10)).pack(anchor="w", padx=19, pady=8)
        self.main = tk.Frame(self.root, bg=COLORS["bg"])
        self.main.pack(side="right", fill="both", expand=True)

    def clear_main(self):
        for child in self.main.winfo_children():
            child.destroy()

    def header(self, title, subtitle):
        top = tk.Frame(self.main, bg=COLORS["bg"])
        top.pack(fill="x", padx=28, pady=(24, 14))
        tk.Label(top, text=title, bg=COLORS["bg"], fg=COLORS["navy"],
                 font=("Segoe UI", 23, "bold")).pack(anchor="w")
        tk.Label(top, text=subtitle, bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

    def scroll_content(self):
        sf = ScrollFrame(self.main)
        sf.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        return sf.inner

    def card(self, parent, title, body, button_text=None, command=None):
        frame = tk.Frame(parent, bg=COLORS["white"], highlightbackground=COLORS["border"],
                         highlightthickness=1, padx=16, pady=14)
        tk.Label(frame, text=title, bg=COLORS["white"], fg=COLORS["navy"],
                 font=("Segoe UI", 12, "bold"), wraplength=700, justify="left").pack(anchor="w")
        tk.Label(frame, text=body, bg=COLORS["white"], fg=COLORS["text"],
                 font=("Segoe UI", 9), wraplength=760, justify="left").pack(anchor="w", pady=(8, 4))
        if button_text:
            ttk.Button(frame, text=button_text, command=command).pack(anchor="w", pady=(8, 0))
        return frame

    def show_dashboard(self):
        self.clear_main()
        self.header("Welcome to AWS Mastery Academy",
                    "A structured learning environment for cloud fundamentals, infrastructure and practical projects.")
        body = self.scroll_content()
        completed = len(self.progress["completed_modules"])
        total = len(MODULES)
        projects_done = len(self.progress["completed_projects"])
        score = self.progress["best_score"]
        stats = tk.Frame(body, bg=COLORS["bg"])
        stats.pack(fill="x", pady=(0, 14))
        for label, value in [("MODULES COMPLETED", f"{completed}/{total}"),
                             ("PROJECTS COMPLETED", str(projects_done)),
                             ("BEST QUIZ SCORE", f"{score}%"),
                             ("QUIZZES TAKEN", str(self.progress["quizzes_taken"]))]:
            box = tk.Frame(stats, bg=COLORS["white"], highlightbackground=COLORS["border"], highlightthickness=1, padx=14, pady=13)
            box.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(box, text=value, bg=COLORS["white"], fg=COLORS["blue"], font=("Segoe UI", 20, "bold")).pack(anchor="w")
            tk.Label(box, text=label, bg=COLORS["white"], fg=COLORS["muted"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        intro = self.card(body, "Your learning strategy",
            "Start with cloud fundamentals, then build confidence in EC2, S3, networking and IAM. "
            "After each module, complete its practice activity. Build projects in a sandbox account, "
            "document what you did and explain the design decisions.")
        intro.pack(fill="x", pady=7)
        row = tk.Frame(body, bg=COLORS["bg"])
        row.pack(fill="x", pady=7)
        self.card(row, "Continue learning", "Study detailed AWS modules with key terms, explanations and practice tasks.",
                  "Open learning modules", self.show_modules).pack(side="left", fill="both", expand=True, padx=(0, 6))
        self.card(row, "Build practical skills", "Follow guided project steps and record completed portfolio work.",
                  "Explore projects", self.show_projects).pack(side="left", fill="both", expand=True, padx=(6, 0))
        self.card(body, "Important AWS safety rule",
            "Before creating resources: check current pricing, set a budget and billing alerts, use MFA, "
            "apply least privilege, avoid real customer data, and delete lab resources when finished. "
            "Budgets and alerts are not a hard spending limit and may not notify instantly.").pack(fill="x", pady=7)
        ttk.Button(body, text="Start the learning roadmap", command=self.show_roadmap).pack(anchor="w", pady=12)

    def show_roadmap(self):
        self.clear_main()
        self.header("AWS Learning Roadmap", "Follow this sequence to build knowledge from fundamentals to job-ready project experience.")
        body = self.scroll_content()
        for number, title, description in LEARNING_PATH:
            frame = tk.Frame(body, bg=COLORS["white"], highlightbackground=COLORS["border"], highlightthickness=1, padx=14, pady=12)
            frame.pack(fill="x", pady=5)
            tk.Label(frame, text=f"{number}.  {title}", bg=COLORS["white"], fg=COLORS["navy"],
                     font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(frame, text=description, bg=COLORS["white"], fg=COLORS["text"],
                     wraplength=820, justify="left").pack(anchor="w", pady=(5, 0))
        self.card(body, "Suggested weekly routine",
                  "Study 4–5 days per week if your schedule allows: 30–45 minutes learning concepts, "
                  "30–60 minutes practising or diagramming, and one longer project session each week. "
                  "Review your notes and explain each service in your own words.").pack(fill="x", pady=10)

    def show_modules(self):
        self.clear_main()
        self.header("AWS Learning Modules", "Choose a topic. Each module includes explanations, terminology and a practical activity.")
        body = self.scroll_content()
        for module in MODULES:
            done = module["title"] in self.progress["completed_modules"]
            frame = self.card(body, ("✓  " if done else "") + module["title"] + f"   [{module['level']}]",
                              module["summary"],
                              "Review module" if done else "Open module",
                              lambda m=module: self.show_module_detail(m))
            frame.pack(fill="x", pady=5)

    def show_module_detail(self, module):
        self.clear_main()
        self.header(module["title"], f"{module['level']} level  •  {module['summary']}")
        body = self.scroll_content()
        for heading, explanation in module["topics"]:
            self.card(body, heading, explanation).pack(fill="x", pady=5)
        self.card(body, "Key terms", module["terms"]).pack(fill="x", pady=5)
        self.card(body, "Put it into practice", module["practice"]).pack(fill="x", pady=5)
        already = module["title"] in self.progress["completed_modules"]
        def mark_done():
            if module["title"] not in self.progress["completed_modules"]:
                self.progress["completed_modules"].append(module["title"])
                save_progress(self.progress)
            messagebox.showinfo("Progress saved", "Module marked as completed.")
            self.show_module_detail(module)
        ttk.Button(body, text="✓ Mark module as completed" if not already else "Completed",
                   command=mark_done, state="disabled" if already else "normal").pack(anchor="w", pady=12)
        ttk.Button(body, text="Back to modules", command=self.show_modules).pack(anchor="w")

    def show_projects(self):
        self.clear_main()
        self.header("AWS Project Challenges", "Hands-on portfolio ideas with guided steps, expected results and cost cautions.")
        body = self.scroll_content()
        for project in PROJECTS:
            done = project["name"] in self.progress["completed_projects"]
            desc = f"{project['level']}  •  {project['time']}\nServices: {', '.join(project['services'])}\n{project['goal']}"
            frame = self.card(body, ("✓  " if done else "") + project["name"], desc,
                              "View project steps", lambda p=project: self.show_project_detail(p))
            frame.pack(fill="x", pady=5)

    def show_project_detail(self, project):
        self.clear_main()
        self.header(project["name"], f"{project['level']} level  •  Estimated learning time: {project['time']}")
        body = self.scroll_content()
        self.card(body, "Project goal", project["goal"]).pack(fill="x", pady=5)
        self.card(body, "AWS services", ", ".join(project["services"])).pack(fill="x", pady=5)
        self.card(body, "Before you start", project["cost"]).pack(fill="x", pady=5)
        step_frame = tk.Frame(body, bg=COLORS["white"], highlightbackground=COLORS["border"], highlightthickness=1, padx=16, pady=14)
        step_frame.pack(fill="x", pady=5)
        tk.Label(step_frame, text="Project checklist", bg=COLORS["white"], fg=COLORS["navy"],
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 8))
        for i, step in enumerate(project["steps"], 1):
            tk.Label(step_frame, text=f"{i}. {step}", bg=COLORS["white"], fg=COLORS["text"],
                     justify="left", wraplength=820, font=("Segoe UI", 9)).pack(anchor="w", pady=5)
        self.card(body, "Definition of done", project["success"]).pack(fill="x", pady=5)
        done = project["name"] in self.progress["completed_projects"]
        def mark_done():
            if project["name"] not in self.progress["completed_projects"]:
                self.progress["completed_projects"].append(project["name"])
                save_progress(self.progress)
            messagebox.showinfo("Project saved", "Project marked as completed. Add your diagrams and notes to your portfolio folder.")
            self.show_project_detail(project)
        ttk.Button(body, text="✓ Mark project completed" if not done else "Completed",
                   command=mark_done, state="disabled" if done else "normal").pack(anchor="w", pady=12)
        ttk.Button(body, text="Back to projects", command=self.show_projects).pack(anchor="w")

    def start_quiz(self):
        self.quiz_questions = random.sample(QUESTIONS, min(20, len(QUESTIONS)))
        self.current_question = 0
        self.quiz_score = 0
        self.quiz_answer = tk.IntVar(value=-1)
        self.show_quiz_question()

    def show_quiz_question(self):
        self.clear_main()
        if self.current_question >= len(self.quiz_questions):
            self.show_quiz_result()
            return
        question, options, correct, explanation = self.quiz_questions[self.current_question]
        self.header("AWS Knowledge Quiz", f"Question {self.current_question + 1} of {len(self.quiz_questions)}  •  Score: {self.quiz_score}")
        body = self.scroll_content()
        progress = ttk.Progressbar(body, maximum=len(self.quiz_questions), value=self.current_question, mode="determinate")
        progress.pack(fill="x", pady=(0, 18))
        card = tk.Frame(body, bg=COLORS["white"], highlightbackground=COLORS["border"], highlightthickness=1, padx=20, pady=20)
        card.pack(fill="x", pady=5)
        tk.Label(card, text=question, bg=COLORS["white"], fg=COLORS["navy"],
                 font=("Segoe UI", 14, "bold"), wraplength=800, justify="left").pack(anchor="w", pady=(0, 16))
        self.quiz_answer.set(-1)
        for idx, option in enumerate(options):
            ttk.Radiobutton(card, text=option, value=idx, variable=self.quiz_answer).pack(anchor="w", pady=7)
        self.quiz_feedback = tk.Label(card, text="", bg=COLORS["white"], fg=COLORS["text"],
                                      font=("Segoe UI", 10), wraplength=800, justify="left")
        self.quiz_feedback.pack(anchor="w", pady=14)
        def submit():
            selected = self.quiz_answer.get()
            if selected < 0:
                messagebox.showwarning("Choose an answer", "Please select an answer before continuing.")
                return
            if selected == correct:
                self.quiz_score += 1
                feedback = "Correct! " + explanation
                color = COLORS["green"]
            else:
                feedback = f"Not quite. Correct answer: {options[correct]}\n{explanation}"
                color = COLORS["red"]
            self.quiz_feedback.configure(text=feedback, fg=color)
            next_button.configure(state="normal")
            submit_button.configure(state="disabled")
        def next_question():
            self.current_question += 1
            self.show_quiz_question()
        submit_button = ttk.Button(body, text="Check answer", command=submit, style="Primary.TButton")
        submit_button.pack(anchor="w", pady=(12, 5))
        next_button = ttk.Button(body, text="Next question", command=next_question, state="disabled")
        next_button.pack(anchor="w")

    def show_quiz_result(self):
        total = len(self.quiz_questions)
        percent = round((self.quiz_score / total) * 100) if total else 0
        self.progress["quizzes_taken"] += 1
        self.progress["best_score"] = max(self.progress["best_score"], percent)
        save_progress(self.progress)
        self.clear_main()
        self.header("Quiz completed", "Review your result and revisit the modules where you want more practice.")
        body = self.scroll_content()
        self.card(body, "Your result", f"{self.quiz_score} out of {total} correct  •  {percent}%").pack(fill="x", pady=7)
        if percent >= 85:
            message = "Excellent work. Keep practising and apply the concepts in a project."
        elif percent >= 65:
            message = "Good progress. Review the explanations for questions you missed, then try again."
        else:
            message = "This is a learning checkpoint. Revisit the beginner modules and take the quiz again."
        self.card(body, "Feedback", message).pack(fill="x", pady=7)
        ttk.Button(body, text="Try another quiz", command=self.start_quiz).pack(anchor="w", pady=10)
        ttk.Button(body, text="Review learning modules", command=self.show_modules).pack(anchor="w")

    def show_career(self):
        self.clear_main()
        self.header("Career & Portfolio", "Turn your learning into evidence you can discuss in an interview.")
        body = self.scroll_content()
        self.card(body, "Suggested role direction",
                  "For Cloud Support, Cloud Operations or Infrastructure Technician roles, focus on networking, "
                  "Linux basics, IAM, EC2, storage, monitoring, backups and incident documentation. "
                  "Your existing IT support experience can help you explain troubleshooting and customer impact.").pack(fill="x", pady=5)
        self.card(body, "Portfolio structure",
                  "Create a folder for each project containing: README.md, architecture diagram, setup steps, "
                  "screenshots with sensitive details hidden, test results, cost notes, security decisions, "
                  "troubleshooting notes and lessons learned. Never publish account IDs, access keys, private keys, "
                  "customer information or secret configuration.").pack(fill="x", pady=5)
        self.card(body, "Projects to highlight on a CV",
                  "1. Secure static website: S3, CloudFront and access control.\n"
                  "2. EC2 Linux web server: compute, SSH security and troubleshooting.\n"
                  "3. VPC network design: CIDR, subnets, routing and security groups.\n"
                  "4. Monitoring lab: CloudWatch alarms and incident runbook.\n"
                  "5. Serverless API: API Gateway, Lambda, DynamoDB and IAM.\n\n"
                  "Describe only work you personally completed. State the tools used, the problem solved and how you tested it.").pack(fill="x", pady=5)
        self.card(body, "Certification study",
                  "A sensible first certification target is AWS Certified Cloud Practitioner (foundational). "
                  "After building fundamentals, consider AWS Certified Solutions Architect – Associate or "
                  "AWS Certified CloudOps Engineer – Associate, depending on your career direction. "
                  "Always check the current AWS exam guide because exam names and objectives can change.").pack(fill="x", pady=5)
        self.card(body, "Interview topics to practise",
                  "Explain the difference between a Region and an Availability Zone; public and private subnets; "
                  "security groups and network ACLs; S3 and EBS; RDS and DynamoDB; IAM users and roles; "
                  "CloudWatch and CloudTrail; and how you would troubleshoot an unreachable EC2 instance.").pack(fill="x", pady=5)
        self.card(body, "A practical 12-week plan",
                  "Weeks 1–2: cloud fundamentals, IAM and billing safety.\n"
                  "Weeks 3–4: EC2, Linux and S3.\n"
                  "Weeks 5–6: VPC, routing, DNS and security.\n"
                  "Weeks 7–8: databases, backups and monitoring.\n"
                  "Weeks 9–10: serverless and automation.\n"
                  "Weeks 11–12: complete two portfolio projects, revise and practise interview explanations.\n\n"
                  "Adjust the pace to your available study time; understanding matters more than rushing.").pack(fill="x", pady=5)

def main():
    root = tk.Tk()
    AWSMasteryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
