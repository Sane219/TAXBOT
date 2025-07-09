# TAXBOT: Indian Income Tax Assistant 🧮

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Live Demo**: [Deploy on Streamlit Cloud](https://share.streamlit.io/)

## 🎯 Overview

TaxBot 2025 is a comprehensive, AI-powered Indian Income Tax Assistant that simplifies tax calculation and provides intelligent tax planning insights. Built with Streamlit, it offers an intuitive interface for calculating tax liabilities under the New Tax Regime for FY 2024-25 and FY 2025-26.

## ✨ Key Features

### 📊 Tax Calculation Engine
- **Accurate Tax Computation**: Implements New Tax Regime rules for FY 2024-25 and FY 2025-26
- **Multiple Income Types**: Supports Salaried, Freelancer, Business, Rental, and Investor income
- **Automated Deductions**: Standard deduction, HRA exemption, and Section 87A rebate
- **Capital Gains**: STCG and LTCG tax calculation with exemptions

### 🔢 Indian Number Formatting
- **Lakhs & Crores Display**: Numbers formatted as Rs. 12,34,567 (Indian system)
- **Proper Comma Placement**: First comma after 3 digits, then every 2 digits
- **Currency Conversion**: Automatic conversion to Indian currency format

### 💡 Smart Tax Tips
- **Context-Aware Advice**: Personalized tips based on your income and tax situation
- **Tax-Saving Recommendations**: Investment opportunities and deduction strategies
- **Compliance Alerts**: Advance tax requirements and filing deadlines

### 📈 Visualizations & Reports
- **Interactive Charts**: Tax breakdown pie charts and income composition
- **Tax Slab Utilization**: Visual representation of tax slab usage
- **PDF Reports**: Downloadable tax summary with tips and calculations
- **Professional Formatting**: Clean, well-structured output

### 🎯 User-Friendly Interface
- **Multi-Tab Navigation**: Organized workflow with Profile, Income, Tax, Reports, and Guidance tabs
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Calculations**: Instant tax computation with live updates

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Windows PowerShell or Command Prompt
- Internet connection for initial setup

### 1. Clone the Repository
```bash
git clone https://github.com/Sane219/TAXBOT.git
cd TAXBOT
```

### 2. Create Virtual Environment
```powershell
# Create virtual environment
python -m venv taxbot_env

# Activate virtual environment (PowerShell)
.\taxbot_env\Scripts\Activate.ps1

# Or for Command Prompt
.\taxbot_env\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Access the App
Open your browser and navigate to: `http://localhost:8501`

## 🌐 Deploy on Streamlit Cloud

### Easy One-Click Deployment
1. Fork this repository to your GitHub account
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and connect your GitHub repository
4. Select:
   - **Repository**: Sane219/TAXBOT
   - **Branch**: main
   - **Main file path**: app.py
5. Click "Deploy!"

Your app will be live at: `https://your-app-name.streamlit.app/`

## 📋 Usage Guide

### Step 1: Profile Setup
1. Select your age group (Below 60, 60 and above, 80 and above)
2. Choose residential status (Resident/Non-Resident)
3. Select financial year (FY 2024-25 or FY 2025-26)
4. Pick your employment type

### Step 2: Income Details
Enter your income details based on employment type:
- **Salaried**: Basic salary, HRA, bonus, rent paid
- **Freelancer/Business**: Net profit, expenses, presumptive taxation
- **Rental**: Rent received, municipal tax, loan interest
- **Investor**: STCG, LTCG, dividends, interest income

### Step 3: Tax Calculation
- Click "Calculate Tax" to compute your tax liability
- View detailed breakdown with Indian formatting
- Get smart tips and recommendations

### Step 4: Reports & Visualization
- Interactive charts showing tax breakdown
- Income composition visualization
- Tax slab utilization graphs
- Download PDF reports

### Step 5: Guidance & Compliance
- Tax payment guidance with step-by-step instructions
- Document checklist based on your profile
- Important tax deadlines and reminders

## 🏗️ Project Structure

```
TAXBOT/
├── app.py                  # Main Streamlit application
├── tax_engine.py          # Core tax calculation logic
├── smart_tips.py          # Smart tips and recommendations
├── visualization.py       # Charts and PDF generation
├── indian_formatter.py    # Indian number formatting utilities
├── test_app.py           # Test suite
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🧪 Testing

Run the test suite to ensure everything is working:
```bash
python test_app.py
```

Expected output:
```
🚀 Starting TaxBot 2025 tests...
✅ All imports successful
✅ Tax engine tests passed
✅ Smart tips tests passed
✅ Visualization tests passed
📊 Test Results: 4/4 tests passed
🎉 All tests passed! TaxBot 2025 is ready to use.
```

## 📦 Dependencies

### Core Libraries
- **Streamlit** (1.28.0): Web application framework
- **Pandas** (2.0.3): Data manipulation and analysis
- **Plotly** (5.17.0): Interactive visualizations
- **NumPy** (1.24.3): Numerical computing

### Visualization & UI
- **Altair** (5.1.1): Statistical visualizations
- **JSON5** (0.9.14): JSON processing
- **Chardet** (5.2.0): Character encoding detection

## 🔧 Configuration

### Tax Regime Settings
The application supports both FY 2024-25 and FY 2025-26 with:
- Updated tax slabs and rates
- Increased rebate limits for FY 2025-26
- Standard deduction of Rs. 75,000
- Section 87A rebate up to Rs. 60,000 (FY 2025-26)

### Customization Options
- Modify tax slabs in `tax_engine.py`
- Add new tip categories in `smart_tips.py`
- Customize charts in `visualization.py`
- Update Indian formatting in `indian_formatter.py`

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Ensure virtual environment is activated
   .\taxbot_env\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Streamlit Not Found**
   ```bash
   # Solution: Use python -m streamlit
   python -m streamlit run app.py
   ```

3. **Port Already in Use**
   ```bash
   # Solution: Use different port
   python -m streamlit run app.py --server.port=8502
   ```

4. **Display Issues**
   - Ensure your browser supports modern CSS
   - Try refreshing the page (Ctrl+F5)
   - Check browser console for errors

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ for the Indian taxpayer community
- Inspired by the need for simplified tax calculation tools
- Thanks to the open-source community for amazing libraries

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on [GitHub](https://github.com/Sane219/TAXBOT/issues)
- Check the troubleshooting section
- Review the test suite output for diagnostics
- Contact: [sanketchauhan0987@gmail.com](mailto:sanketchauhan0987@gmail.com)

## 👤 Author

**Sanket Chauhan** ([@Sane219](https://github.com/Sane219))
- Email: sanketchauhan0987@gmail.com
- GitHub: [Sane219](https://github.com/Sane219)

---

**Made with ❤️ for Indian Taxpayers** | TAXBOT © 2025
