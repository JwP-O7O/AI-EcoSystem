#!/data/data/com.termux/files/usr/bin/bash

# ============================================================
# Agent Zero - Android/Termux Setup Script
# Versie: 1.0 - November 26, 2025
# ============================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in Termux
check_termux() {
    if [ ! -d "/data/data/com.termux" ]; then
        print_error "This script must be run in Termux on Android!"
        exit 1
    fi
    print_success "Running in Termux ✓"
}

# Check Python
check_python() {
    print_info "Checking Python installation..."
    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        print_success "Python $PYTHON_VERSION found ✓"
    else
        print_error "Python not found!"
        print_info "Installing Python..."
        pkg install -y python
    fi
}

# Check pip
check_pip() {
    print_info "Checking pip installation..."
    if command -v pip &> /dev/null; then
        print_success "pip found ✓"
    else
        print_error "pip not found!"
        print_info "Installing pip..."
        pkg install -y python-pip
    fi
}

# Install system dependencies
install_system_deps() {
    print_header "📦 Installing System Dependencies"

    print_info "Updating package lists..."
    pkg update -y

    print_info "Installing essential packages..."
    pkg install -y \
        python \
        python-pip \
        git \
        openssh \
        openssl \
        libffi \
        rust \
        binutils \
        clang \
        wget \
        curl \
        libxml2 \
        libxslt \
        termux-api

    print_success "System dependencies installed ✓"
}

# Check and advise on Wake Lock
check_wakelock() {
    print_header "🔋 Power Management"
    
    if command -v termux-wake-lock &> /dev/null; then
        print_info "It is recommended to acquire a wake lock to prevent Android from killing the process."
        echo -e "${YELLOW}Run 'termux-wake-lock' before long sessions.${NC}"
        # Optional: Auto-acquire? Better to just advise for now.
    else
        print_warning "termux-api not found. Install 'Termux:API' app from F-Droid for better stability."
    fi
}

# Install Python dependencies
install_python_deps() {
    print_header "🐍 Installing Python Dependencies"

    # Upgrade pip first
    print_info "Upgrading pip..."
    pip install --upgrade pip

    # Determine project root
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    
    print_info "Project root determined as: $PROJECT_ROOT"
    cd "$PROJECT_ROOT"

    if [ -f "android-versie/requirements-android.txt" ]; then
        print_info "Installing from requirements-android.txt..."
        pip install -r android-versie/requirements-android.txt
        print_success "Python packages installed ✓"
    else
        print_error "requirements-android.txt not found in $PROJECT_ROOT/android-versie/"
        exit 1
    fi
}

# Setup .env file
setup_env() {
    print_header "⚙️  Configuring Environment"

    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    
    ENV_FILE="$PROJECT_ROOT/android-versie/config/.env"
    ENV_EXAMPLE="$PROJECT_ROOT/android-versie/config/.env.example"

    if [ -f "$ENV_FILE" ]; then
        print_warning ".env file already exists"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing .env file"
            return
        fi
    fi

    if [ -f "$ENV_EXAMPLE" ]; then
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        print_success ".env file created from template ✓"
        print_warning "⚠️  IMPORTANT: Edit android-versie/config/.env and add your API keys!"
    else
        print_error ".env.example not found at $ENV_EXAMPLE"
    fi
}

# Create necessary directories
create_directories() {
    print_header "📁 Creating Directories"

    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    cd "$PROJECT_ROOT"

    mkdir -p work_dir
    mkdir -p logs
    mkdir -p memory
    mkdir -p knowledge/custom

    print_success "Directories created ✓"
}

# Make scripts executable
make_executable() {
    print_header "🔧 Setting Permissions"

    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    cd "$PROJECT_ROOT/android-versie"

    chmod +x run_android_cli.py
    chmod +x scripts/*.sh

    print_success "Permissions set ✓"
}

# Test installation
test_installation() {
    print_header "🧪 Testing Installation"

    print_info "Testing Python imports..."
    python -c "import anthropic; print('✅ anthropic')" 2>/dev/null || print_warning "anthropic not imported"
    python -c "import openai; print('✅ openai')" 2>/dev/null || print_warning "openai not imported"
    python -c "import langchain; print('✅ langchain')" 2>/dev/null || print_warning "langchain not imported"
    python -c "import flask; print('✅ flask')" 2>/dev/null || print_warning "flask not imported"

    print_success "Import tests completed ✓"
}

# Print next steps
print_next_steps() {
    print_header "🎉 Installation Complete!"

    echo -e "${GREEN}Agent Zero is ready for Android/Termux!${NC}"
    echo ""
    echo -e "${YELLOW}📝 Next Steps:${NC}"
    echo ""
    echo "1. Configure your API keys:"
    echo -e "   ${CYAN}nano android-versie/config/.env${NC}"
    echo ""
    echo "2. Read the documentation:"
    echo -e "   ${CYAN}cat android-versie/docs/QUICK_START.md${NC}"
    echo ""
    echo "3. Start Agent Zero:"
    echo -e "   ${CYAN}cd /data/data/com.termux/files/home/AI-EcoSystem${NC}"
    echo -e "   ${CYAN}python android-versie/run_android_cli.py${NC}"
    echo ""
    echo "4. Or use the quick launcher:"
    echo -e "   ${CYAN}bash android-versie/scripts/start.sh${NC}"
    echo ""
    print_info "For help and troubleshooting, see:"
    echo -e "   ${CYAN}android-versie/docs/TROUBLESHOOTING.md${NC}"
    echo ""
}

# Main execution
main() {
    print_header "🤖 Agent Zero - Android/Termux Setup"

    print_info "This script will install and configure Agent Zero for Android/Termux"
    echo ""
    read -p "Continue? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_info "Setup cancelled"
        exit 0
    fi

    # Run setup steps
    check_termux
    check_python
    check_pip
    install_system_deps
    install_python_deps
    create_directories
    setup_env
    make_executable
    test_installation
    check_wakelock
    print_next_steps
}

# Run main function
main
