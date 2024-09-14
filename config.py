# config.py

AGENT_CATEGORIES = [
    "Smart Manufacturing",
    "Industrial IoT",
    "Predictive Maintenance",
    "Digital Twin",
    "Robotics and Automation",
    "AI and Machine Learning",
    "Cybersecurity",
    "Cloud Computing",
    "Big Data Analytics",
    "Additive Manufacturing",
    "Augmented Reality",
    "Blockchain",
    "Energy Efficiency",
    "Sustainable Supply Chain",
    "Circular Economy",
    "Waste Reduction",
    "Water Management",
    "Emissions Control"
]

DUMMY_AGENTS = [
    {
        "id": "001",
        "name": "SmartFactory Solutions",
        "categories": ["Smart Manufacturing", "Industrial IoT"],
        "specialization": "Implements comprehensive smart factory solutions, integrating IoT sensors, real-time monitoring, and adaptive manufacturing processes.",
        "initial_bid_range": (100000, 250000),
        "reduction_strategy": "percentage",
        "min_bid": 90000
    },
    {
        "id": "002",
        "name": "PredictiveTech",
        "categories": ["Predictive Maintenance", "AI and Machine Learning"],
        "specialization": "Develops AI-driven predictive maintenance systems for industrial equipment, reducing downtime and extending machinery lifespan.",
        "initial_bid_range": (80000, 180000),
        "reduction_strategy": "fixed",
        "min_bid": 70000
    },
    {
        "id": "003",
        "name": "DigitalTwin Innovators",
        "categories": ["Digital Twin", "Big Data Analytics"],
        "specialization": "Creates digital twin solutions for complex industrial processes, enabling real-time simulation and optimization.",
        "initial_bid_range": (120000, 280000),
        "reduction_strategy": "random",
        "min_bid": 100000
    },
    {
        "id": "004",
        "name": "RoboSustain",
        "categories": ["Robotics and Automation", "Energy Efficiency"],
        "specialization": "Designs and implements energy-efficient robotic systems for automated manufacturing and warehouse operations.",
        "initial_bid_range": (150000, 350000),
        "reduction_strategy": "percentage",
        "min_bid": 130000
    },
    {
        "id": "005",
        "name": "CyberShield Industries",
        "categories": ["Cybersecurity", "Industrial IoT"],
        "specialization": "Provides robust cybersecurity solutions for industrial IoT networks, ensuring data integrity and system protection.",
        "initial_bid_range": (90000, 200000),
        "reduction_strategy": "fixed",
        "min_bid": 80000
    },
    {
        "id": "006",
        "name": "CloudManufacture",
        "categories": ["Cloud Computing", "Smart Manufacturing"],
        "specialization": "Offers cloud-based manufacturing platforms, enabling distributed production and real-time supply chain management.",
        "initial_bid_range": (110000, 260000),
        "reduction_strategy": "random",
        "min_bid": 95000
    },
    {
        "id": "007",
        "name": "DataDriven Sustainability",
        "categories": ["Big Data Analytics", "Sustainable Supply Chain"],
        "specialization": "Utilizes big data analytics to optimize supply chains for sustainability, reducing waste and improving efficiency.",
        "initial_bid_range": (100000, 230000),
        "reduction_strategy": "percentage",
        "min_bid": 85000
    },
    {
        "id": "008",
        "name": "3DPrint Green",
        "categories": ["Additive Manufacturing", "Waste Reduction"],
        "specialization": "Provides sustainable 3D printing solutions, using recycled materials and optimizing designs for minimal waste.",
        "initial_bid_range": (70000, 160000),
        "reduction_strategy": "fixed",
        "min_bid": 60000
    },
    {
        "id": "009",
        "name": "AugmentedOps",
        "categories": ["Augmented Reality", "Smart Manufacturing"],
        "specialization": "Develops AR solutions for industrial operations, improving worker efficiency and reducing errors in complex tasks.",
        "initial_bid_range": (85000, 190000),
        "reduction_strategy": "random",
        "min_bid": 75000
    },
    {
        "id": "010",
        "name": "BlockchainTraceability",
        "categories": ["Blockchain", "Sustainable Supply Chain"],
        "specialization": "Implements blockchain solutions for supply chain traceability, ensuring ethical sourcing and sustainable practices.",
        "initial_bid_range": (95000, 220000),
        "reduction_strategy": "percentage",
        "min_bid": 80000
    },
    {
        "id": "011",
        "name": "EnergyAI Optimizers",
        "categories": ["Energy Efficiency", "AI and Machine Learning"],
        "specialization": "Uses AI to optimize energy consumption in industrial processes, significantly reducing carbon footprint.",
        "initial_bid_range": (110000, 250000),
        "reduction_strategy": "fixed",
        "min_bid": 95000
    },
    {
        "id": "012",
        "name": "CircularTech Solutions",
        "categories": ["Circular Economy", "Smart Manufacturing"],
        "specialization": "Designs manufacturing processes and products for circular economy, maximizing resource reuse and recycling.",
        "initial_bid_range": (120000, 270000),
        "reduction_strategy": "random",
        "min_bid": 100000
    },
    {
        "id": "013",
        "name": "ZeroWaste Manufacturing",
        "categories": ["Waste Reduction", "Industrial IoT"],
        "specialization": "Implements IoT-based waste reduction solutions in manufacturing, aiming for zero-waste production.",
        "initial_bid_range": (90000, 200000),
        "reduction_strategy": "percentage",
        "min_bid": 75000
    },
    {
        "id": "014",
        "name": "AquaIndustry 4.0",
        "categories": ["Water Management", "Smart Manufacturing"],
        "specialization": "Develops smart water management systems for industries, optimizing usage and implementing advanced recycling technologies.",
        "initial_bid_range": (100000, 230000),
        "reduction_strategy": "fixed",
        "min_bid": 85000
    },
    {
        "id": "015",
        "name": "CleanAir Industria",
        "categories": ["Emissions Control", "Industrial IoT"],
        "specialization": "Provides IoT-based emissions monitoring and control systems, ensuring regulatory compliance and minimizing environmental impact.",
        "initial_bid_range": (110000, 260000),
        "reduction_strategy": "random",
        "min_bid": 95000
    },
    {
        "id": "016",
        "name": "AI Quality Control",
        "categories": ["AI and Machine Learning", "Smart Manufacturing"],
        "specialization": "Implements AI-driven quality control systems, reducing defects and optimizing resource use in manufacturing.",
        "initial_bid_range": (95000, 220000),
        "reduction_strategy": "percentage",
        "min_bid": 80000
    },
    {
        "id": "017",
        "name": "CognitiveMaintenance Pro",
        "categories": ["Predictive Maintenance", "Big Data Analytics"],
        "specialization": "Offers cognitive computing solutions for equipment maintenance, predicting failures and optimizing maintenance schedules.",
        "initial_bid_range": (105000, 240000),
        "reduction_strategy": "fixed",
        "min_bid": 90000
    },
    {
        "id": "018",
        "name": "SupplyChainAI",
        "categories": ["AI and Machine Learning", "Sustainable Supply Chain"],
        "specialization": "Uses AI to optimize entire supply chains for sustainability, from sourcing to delivery, minimizing environmental impact.",
        "initial_bid_range": (115000, 270000),
        "reduction_strategy": "random",
        "min_bid": 100000
    },
    {
        "id": "019",
        "name": "EdgeCompute Green",
        "categories": ["Industrial IoT", "Energy Efficiency"],
        "specialization": "Provides edge computing solutions for industrial IoT, optimizing data processing and reducing energy consumption.",
        "initial_bid_range": (85000, 190000),
        "reduction_strategy": "percentage",
        "min_bid": 70000
    },
    {
        "id": "020",
        "name": "Quantum Optimization Systems",
        "categories": ["AI and Machine Learning", "Energy Efficiency"],
        "specialization": "Utilizes quantum computing algorithms for complex industrial optimization problems, significantly improving efficiency.",
        "initial_bid_range": (200000, 450000),
        "reduction_strategy": "fixed",
        "min_bid": 180000
    }
]