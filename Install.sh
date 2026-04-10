#!/bin/bash

# ============================================
# HK-vi18 VPS Bot Installation Script
# Made by Ankit Ex. & PowerDev
# Discord ID: PowerDev
# Version: 18.0
# ============================================

# Rainbow color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
ORANGE='\033[0;33m'
PURPLE='\033[0;35m'
PINK='\033[0;35m'
BOLD='\033[1m'
BLINK='\033[5m'
NC='\033[0m'

# Rainbow animation function
rainbow_animation() {
    local text="$1"
    local colors=($RED $GREEN $YELLOW $BLUE $MAGENTA $CYAN)
    for ((i=0; i<${#text}; i++)); do
        color_index=$((i % ${#colors[@]}))
        echo -ne "${colors[$color_index]}${text:$i:1}${NC}"
        sleep 0.02
    done
    echo
}

# Big Rainbow Title Function
print_rainbow_title() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                                                          ║"
    
    # Line 1 - HK
    echo -ne "║  "
    rainbow_animation "HH   HH  KKKKKK   VV     VV  IIIIIII   8888888   IIIIIII     "
    echo "║"
    
    # Line 2
    echo -ne "║  "
    rainbow_animation "HH   HH  KK   KK   VV   VV     III     88   88     III       "
    echo "║"
    
    # Line 3
    echo -ne "║  "
    rainbow_animation "HHHHHHH  KKKKKK     VV VV      III     8888888     III       "
    echo "║"
    
    # Line 4
    echo -ne "║  "
    rainbow_animation "HH   HH  KK  KK      VVV       III     88   88     III       "
    echo "║"
    
    # Line 5
    echo -ne "║  "
    rainbow_animation "HH   HH  KK   KK      V      IIIIIII   8888888   IIIIIII     "
    echo "║"
    
    echo "║                                                                                                          ║"
    echo "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════╣"
    echo -e "║  ${BOLD}${WHITE}██████╗ ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗███╗   ███╗███████╗███╗   ██╗████████╗${NC}  ║"
    echo -e "║  ${BOLD}${WHITE}██╔══██╗██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║   ██║████╗ ████║██╔════╝████╗  ██║╚══██╔══╝${NC}  ║"
    echo -e "║  ${BOLD}${WHITE}██████╔╝██████╔╝█████╗  ██║  ██║██║     ██║   ██║██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ${NC}  ║"
    echo -e "║  ${BOLD}${WHITE}██╔═══╝ ██╔══██╗██╔══╝  ██║  ██║██║     ██║   ██║██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ${NC}  ║"
    echo -e "║  ${BOLD}${WHITE}██║     ██║  ██║███████╗██████╔╝███████╗╚██████╔╝╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ${NC}  ║"
    echo -e "║  ${BOLD}${WHITE}╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ${NC}  ║"
    echo "║                                                                                                          ║"
    echo "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════╣"
    echo -e "║  ${BOLD}${WHITE}✨ VPS Management System v2.0 ✨                                                        ${NC}║"
    echo -e "║  ${BOLD}${WHITE}🎯 Node: HK-vi18 | RAM: 2GB/Instance | CPU: 2 Cores/Instance                           ${NC}║"
    echo -e "║  ${BOLD}${WHITE}💜 Made with 💜 by AryanDEv007                                                        ${NC}║"
    echo -e "║  ${BOLD}${WHITE}🆔 Discord ID: devaru007 | GitHub:                                                   ${NC}║"
    echo "╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Loading animation
loading_animation() {
    local message="$1"
    local chars=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
    for i in {1..20}; do
        echo -ne "\r${CYAN}${chars[$i % 10]} ${message}${NC}"
        sleep 0.1
    done
    echo -e "\r${GREEN}✓ ${message}${NC}"
}

# Progress bar
progress_bar() {
    local duration=$1
    local message=$2
    echo -ne "${CYAN}${message}${NC} "
    for ((i=0; i<=duration; i++)); do
        echo -ne "${GREEN}█${NC}"
        sleep 0.05
    done
    echo -e " ${GREEN}100%${NC}"
}

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 completed successfully${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        exit 1
    fi
}

# Function to create Dockerfiles with rainbow animation
create_dockerfiles() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║              🐳 Creating Docker Images & Files                    ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    # Create directory if not exists
    mkdir -p ~/hk-vi18-bot/dockerfiles
    cd ~/hk-vi18-bot
    
    # Ubuntu Dockerfile
    echo -ne "${YELLOW}Creating Ubuntu 22.04 Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.ubuntu << 'EOF'
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    openssh-server sudo curl wget git vim htop net-tools tmate \
    python3 python3-pip build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # Debian Dockerfile
    echo -ne "${YELLOW}Creating Debian 12 Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.debian << 'EOF'
FROM debian:12
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    openssh-server sudo curl wget git vim htop net-tools tmate \
    python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # Alpine Dockerfile
    echo -ne "${YELLOW}Creating Alpine Linux Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.alpine << 'EOF'
FROM alpine:latest
RUN apk add --no-cache openssh-server sudo curl wget git vim htop tmate \
    python3 py3-pip && \
    ssh-keygen -A && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # Arch Dockerfile
    echo -ne "${YELLOW}Creating Arch Linux Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.arch << 'EOF'
FROM archlinux:latest
RUN pacman -Syu --noconfirm openssh sudo curl wget git vim htop net-tools tmate \
    python python-pip && \
    systemctl enable sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # Kali Dockerfile
    echo -ne "${YELLOW}Creating Kali Linux Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.kali << 'EOF'
FROM kalilinux/kali-rolling
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    openssh-server sudo curl wget git vim htop net-tools tmate \
    kali-tools-top10 python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # Fedora Dockerfile
    echo -ne "${YELLOW}Creating Fedora 39 Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.fedora << 'EOF'
FROM fedora:39
RUN dnf install -y openssh-server sudo curl wget git vim htop net-tools tmate \
    python3 python3-pip && \
    systemctl enable sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # CentOS Dockerfile
    echo -ne "${YELLOW}Creating CentOS Stream 9 Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.centos << 'EOF'
FROM centos:stream9
RUN dnf install -y openssh-server sudo curl wget git vim htop net-tools tmate \
    python3 python3-pip && \
    systemctl enable sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    # Rocky Linux Dockerfile
    echo -ne "${YELLOW}Creating Rocky Linux 9 Dockerfile...${NC} "
    cat > dockerfiles/Dockerfile.rocky << 'EOF'
FROM rockylinux:9
RUN dnf install -y openssh-server sudo curl wget git vim htop net-tools tmate \
    python3 python3-pip && \
    systemctl enable sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF
    echo -e "${GREEN}✓${NC}"
    
    echo -e "\n${GREEN}✅ All 8 Dockerfiles created successfully!${NC}\n"
}

# Function to build Docker images
build_docker_images() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║              🔨 Building Docker Images                          ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    cd ~/hk-vi18-bot
    
    # Array of OS names
    os_list=("ubuntu" "debian" "alpine" "arch" "kali" "fedora" "centos" "rocky")
    
    for os in "${os_list[@]}"; do
        echo -ne "${YELLOW}Building ${os}-vps image...${NC} "
        docker build -t ${os}-vps -f dockerfiles/Dockerfile.${os} . > /tmp/docker_build_${os}.log 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗ Failed (check /tmp/docker_build_${os}.log)${NC}"
        fi
        progress_bar 2 "  Progress"
    done
    
    echo -e "\n${GREEN}✅ All Docker images built successfully!${NC}\n"
}

# Function to install dependencies
install_dependencies() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║              📦 Installing Dependencies                         ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    echo -ne "${YELLOW}Updating system packages...${NC} "
    sudo apt update > /dev/null 2>&1
    echo -e "${GREEN}✓${NC}"
    
    echo -ne "${YELLOW}Installing Python3 and pip...${NC} "
    sudo apt install -y python3 python3-pip python3-venv > /dev/null 2>&1
    echo -e "${GREEN}✓${NC}"
    
    echo -ne "${YELLOW}Installing Docker...${NC} "
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh > /dev/null 2>&1
        sudo sh get-docker.sh > /dev/null 2>&1
        sudo usermod -aG docker $USER
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${GREEN}✓ Already installed${NC}"
    fi
    
    echo -ne "${YELLOW}Installing Python packages...${NC} "
    pip3 install discord.py psutil > /dev/null 2>&1
    echo -e "${GREEN}✓${NC}"
    
    echo -ne "${YELLOW}Installing screen for background execution...${NC} "
    sudo apt install -y screen > /dev/null 2>&1
    echo -e "${GREEN}✓${NC}"
    
    echo -e "\n${GREEN}✅ All dependencies installed successfully!${NC}\n"
}

# Function to create configuration files
create_config_files() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║              ⚙️  Creating Configuration Files                     ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    cd ~/hk-vi18-bot
    
    # Create database file
    touch database.txt
    echo -e "${GREEN}✓ Database file created${NC}"
    
    # Create nodes.json
    cat > nodes.json << 'EOF'
{
    "HK-vi18": {
        "ip": "localhost",
        "port": 2375,
        "status": "online",
        "type": "master",
        "created_at": ""
    }
}
EOF
    echo -e "${GREEN}✓ Nodes configuration created${NC}"
    
    # Create start script
    cat > start_bot.sh << 'EOF'
#!/bin/bash
cd ~/hk-vi18-bot
echo "Starting HK-vi18 VPS Bot..."
python3 bot.py
EOF
    chmod +x start_bot.sh
    echo -e "${GREEN}✓ Start script created${NC}"
    
    # Create systemd service file
    cat > hk-vi18-bot.service << 'EOF'
[Unit]
Description=HK-vi18 VPS Management Bot
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/hk-vi18
ExecStart=/usr/bin/python3 /home/ubuntu/hk-vi18/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    echo -e "${GREEN}✓ Systemd service file created${NC}"
    
    echo -e "\n${GREEN}✅ Configuration files created successfully!${NC}\n"
}

# Function to show next steps
show_next_steps() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║              🎉 Installation Complete!                           ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    echo -e "${GREEN}${BOLD}✓ Dockerfiles created in: ~/hk-vi18-bot/dockerfiles/${NC}"
    echo -e "${GREEN}${BOLD}✓ Docker images built: 8 OS images${NC}"
    echo -e "${GREEN}${BOLD}✓ Dependencies installed${NC}"
    echo -e "${GREEN}${BOLD}✓ Configuration files created${NC}\n"
    
    echo -e "${YELLOW}${BOLD}📋 NEXT STEPS:${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}1. Download the bot.py file:${NC}"
    echo -e "   ${GREEN}wget https://raw.githubusercontent.com/AnkitKing7/bot.py -O ~/hk-vi18/bot.py${NC}\n"
    
    echo -e "${WHITE}2. Edit bot.py and add your configuration:${NC}"
    echo -e "   ${GREEN}nano ~/hk-vi18/bot.py${NC}\n"
    
    echo -e "${WHITE}3. Add your Discord Bot Token:${NC}"
    echo -e "   ${GREEN}TOKEN = 'YOUR_BOT_TOKEN_HERE'${NC}\n"
    
    echo -e "${WHITE}4. Add your Channel IDs:${NC}"
    echo -e "   ${GREEN}DEPLOY_CHANNEL_IDS = [123456789]  # Channels for /deploy command${NC}"
    echo -e "   ${GREEN}LOGS_CHANNEL_IDS = [123456789]    # Channels for bot logs${NC}\n"
    
    echo -e "${WHITE}5. Add your Admin User IDs:${NC}"
    echo -e "   ${GREEN}ADMIN_IDS = [1234567890]  # Your Discord User ID${NC}\n"
    
    echo -e "${WHITE}6. Run the bot:${NC}"
    echo -e "   ${GREEN}cd ~/hk-vi18${NC}"
    echo -e "   ${GREEN}python3 bot.py${NC}\n"
    
    echo -e "${WHITE}7. Or run in background with screen:${NC}"
    echo -e "   ${GREEN}screen -S hk-vi18${NC}"
    echo -e "   ${GREEN}cd ~/hk-vi18 && python3 bot.py${NC}"
    echo -e "   ${GREEN}Press Ctrl+A, then D to detach${NC}\n"
    
    echo -e "${WHITE}8. Or install as systemd service:${NC}"
    echo -e "   ${GREEN}sudo cp ~/hk-vi18/hk-vi18.service /etc/systemd/system/${NC}"
    echo -e "   ${GREEN}sudo systemctl daemon-reload${NC}"
    echo -e "   ${GREEN}sudo systemctl enable hk-vi18${NC}"
    echo -e "   ${GREEN}sudo systemctl start hk-vi18${NC}"
    echo -e "   ${GREEN}sudo systemctl status hk-vi18${NC}\n"
    
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}${BOLD}💜 Made with Love by AryanDev ${NC}"
    echo -e "${PURPLE}${BOLD}🆔 Discord: devaru007 | GitHub: ${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Function to verify installation
verify_installation() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║              🔍 Verifying Installation                          ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    echo -ne "${YELLOW}Checking Docker...${NC} "
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${REDyour-r
    fi
    
    echo -ne "${YELLOW}Checking Python...${NC} "
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
    
    echo -ne "${YELLOW}Checking Docker images...${NC} "
    image_count=$(docker images | grep -c "vps" || echo "0")
    if [ $image_count -ge 5 ]; then
        echo -e "${GREEN}✓ ($image_count images)${NC}"
    else
        echo -e "${YELLOW}⚠ ($image_count images)${NC}"
    fi
    
    echo -ne "${YELLOW}Checking Dockerfiles...${NC} "
    dockerfile_count=$(ls ~/hk-vi18/dockerfiles/ 2>/dev/null | wc -l)
    if [ $dockerfile_count -eq 8 ]; then
        echo -e "${GREEN}✓ ($dockerfile_count files)${NC}"
    else
        echo -e "${YELLOW}⚠ ($dockerfile_count files)${NC}"
    fi
    
    echo -ne "${YELLOW}Checking configuration...${NC} "
    if [ -f ~/hk-vi18/database.txt ] && [ -f ~/hk-vi18/nodes.json ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
    
    echo -e "\n${GREEN}✅ Installation verification complete!${NC}\n"
}

# Main installation function
main() {
    # Print rainbow title
    print_rainbow_title
    
    echo -e "${CYAN}${BOLD}Starting HK-vi18 VPS Bot Installation...${NC}\n"
    sleep 2
    
    # Create main directory
    mkdir -p ~/hk-vi18
    cd ~/hk-vi18
    
    # Run installation steps
    install_dependencies
    sleep 1
    
    create_dockerfiles
    sleep 1
    
    build_docker_images
    sleep 1
    
    create_config_files
    sleep 1
    
    verify_installation
    sleep 1
    
    show_next_steps
}

# Run main function
main
