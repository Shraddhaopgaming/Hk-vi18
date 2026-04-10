#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HK-vi18 VPS Management Bot
Made by Ankit Ex. & PowerDev
Discord ID: PowerDev
Version: 3.0
"""

import random
import subprocess
import os
import discord
from discord.ext import commands, tasks
import asyncio
from discord import app_commands
import psutil
from datetime import datetime, timedelta
import json
import re
import secrets
import string
import time
import platform
import socket

# ============================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================

TOKEN = ''  # ADD YOUR BOT TOKEN HERE

# Node Configuration
NODE_NAME = "HK-vi18"
RAM_LIMIT = '2g'
CPU_LIMIT = '2'
STORAGE_LIMIT = '10g'
SERVER_LIMIT = 12
INACTIVE_TIMEOUT_HOURS = 4

# Channel Configuration - ADD YOUR CHANNEL IDs
DEPLOY_CHANNEL_IDS = []  # Channels where /deploy can be used
LOGS_CHANNEL_IDS = []    # Channels for bot logs

# Admin Configuration - ADD YOUR USER IDs
ADMIN_IDS = []           # Your Discord User ID(s)

# File paths
database_file = 'database.txt'
nodes_file = 'nodes.json'
config_file = 'config.json'

# ============================================
# BOT INITIALIZATION
# ============================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Color constants
EMBED_COLOR = 0x9B59B6      # Purple
SUCCESS_COLOR = 0x00FF00    # Green
ERROR_COLOR = 0xFF0000      # Red
WARNING_COLOR = 0xFFA500    # Orange
INFO_COLOR = 0x3498DB       # Blue
NODE_COLOR = 0x00CED1       # Dark Turquoise
VPS_COLOR = 0x4B0082        # Indigo

# ============================================
# IMAGE URLs
# ============================================

BANNER_IMAGE = "https://i.imgur.com/6XrJ7vP.png"
VPS_MANAGEMENT_IMAGE = "https://i.imgur.com/9k2zJpM.png"
NODE_STATUS_IMAGE = "https://i.imgur.com/4YpX8nL.png"
HELP_BANNER = "https://i.imgur.com/7QwR2tK.png"
MADE_BY_IMAGE = "https://i.imgur.com/3Xy8ZmA.png"
NODE_IMAGE = "https://i.imgur.com/node-icon.png"
CPU_IMAGE = "https://i.imgur.com/cpu-icon.png"
RAM_IMAGE = "https://i.imgur.com/ram-icon.png"
DISK_IMAGE = "https://i.imgur.com/disk-icon.png"
SUCCESS_IMAGE = "https://i.imgur.com/success-icon.png"
ERROR_IMAGE = "https://i.imgur.com/error-icon.png"
WARNING_IMAGE = "https://i.imgur.com/warning-icon.png"

# OS Icons/Images
OS_IMAGES = {
    "ubuntu": "https://i.imgur.com/ubuntu-logo.png",
    "debian": "https://i.imgur.com/debian-logo.png",
    "alpine": "https://i.imgur.com/alpine-logo.png",
    "arch": "https://i.imgur.com/arch-logo.png",
    "kali": "https://i.imgur.com/kali-logo.png",
    "fedora": "https://i.imgur.com/fedora-logo.png",
    "centos": "https://i.imgur.com/centos-logo.png",
    "rocky": "https://i.imgur.com/rocky-logo.png",
    "almalinux": "https://i.imgur.com/almalinux-logo.png",
    "opensuse": "https://i.imgur.com/opensuse-logo.png"
}

# ============================================
# OS CONFIGURATION
# ============================================

OS_OPTIONS = {
    "ubuntu": {
        "image": "ubuntu-vps",
        "name": "Ubuntu 22.04 LTS",
        "emoji": "🐧",
        "thumbnail": OS_IMAGES["ubuntu"],
        "color": 0xE95420,
        "description": "Most popular Linux distribution, great for beginners and professionals",
        "features": ["LTS Support", "APT Package Manager", "Large Community"]
    },
    "debian": {
        "image": "debian-vps",
        "name": "Debian 12 Bookworm",
        "emoji": "🦕",
        "thumbnail": OS_IMAGES["debian"],
        "color": 0xA80030,
        "description": "Stable and secure, perfect for production servers",
        "features": ["Rock Solid Stability", "APT Package Manager", "Security Focused"]
    },
    "alpine": {
        "image": "alpine-vps",
        "name": "Alpine Linux",
        "emoji": "⛰️",
        "thumbnail": OS_IMAGES["alpine"],
        "color": 0x0D597F,
        "description": "Lightweight and secure, minimal footprint",
        "features": ["~5MB Size", "APK Package Manager", "Musl Libc"]
    },
    "arch": {
        "image": "arch-vps",
        "name": "Arch Linux",
        "emoji": "🎯",
        "thumbnail": OS_IMAGES["arch"],
        "color": 0x1793D1,
        "description": "Rolling release, always up-to-date packages",
        "features": ["Rolling Release", "AUR Access", "Pacman Package Manager"]
    },
    "kali": {
        "image": "kali-vps",
        "name": "Kali Linux",
        "emoji": "💣",
        "thumbnail": OS_IMAGES["kali"],
        "color": 0x557C94,
        "description": "Penetration testing and security auditing OS",
        "features": ["Security Tools", "Kali Tools", "Ethical Hacking"]
    },
    "fedora": {
        "image": "fedora-vps",
        "name": "Fedora 39",
        "emoji": "🎩",
        "thumbnail": OS_IMAGES["fedora"],
        "color": 0x294172,
        "description": "Cutting-edge features, sponsored by Red Hat",
        "features": ["Latest Software", "DNF Package Manager", "SELinux Enabled"]
    },
    "centos": {
        "image": "centos-vps",
        "name": "CentOS Stream 9",
        "emoji": "🟡",
        "thumbnail": OS_IMAGES["centos"],
        "color": 0x262577,
        "description": "Enterprise Linux, RHEL compatible",
        "features": ["Enterprise Ready", "DNF Package Manager", "Long Term Support"]
    },
    "rocky": {
        "image": "rocky-vps",
        "name": "Rocky Linux 9",
        "emoji": "🪨",
        "thumbnail": OS_IMAGES["rocky"],
        "color": 0x10B981,
        "description": "Community enterprise OS, RHEL compatible",
        "features": ["Enterprise Grade", "DNF Package Manager", "Stable & Secure"]
    },
    "almalinux": {
        "image": "almalinux-vps",
        "name": "AlmaLinux 9",
        "emoji": "🦌",
        "thumbnail": OS_IMAGES["almalinux"],
        "color": 0x1C69B4,
        "description": "Open source enterprise Linux",
        "features": ["RHEL Compatible", "DNF Package Manager", "Community Driven"]
    },
    "opensuse": {
        "image": "opensuse-vps",
        "name": "OpenSUSE Leap",
        "emoji": "🦎",
        "thumbnail": OS_IMAGES["opensuse"],
        "color": 0x73BA25,
        "description": "Stable and user-friendly Linux distribution",
        "features": ["YaST Tools", "Zypper Package Manager", "Open Build Service"]
    }
}

# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_random_port():
    return random.randint(1025, 65535)

def generate_ssh_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for i in range(length))

def generate_container_id():
    return secrets.token_hex(8)

def add_to_database(user, container_id, ssh_command, password=None, os_name=None):
    timestamp = datetime.now().isoformat()
    with open(database_file, 'a') as f:
        if password:
            f.write(f"{user}|{container_id}|{ssh_command}|{password}|{NODE_NAME}|{os_name}|{timestamp}\n")
        else:
            f.write(f"{user}|{container_id}|{ssh_command}|none|{NODE_NAME}|{os_name}|{timestamp}\n")

def remove_from_database(container_id):
    if not os.path.exists(database_file):
        return
    with open(database_file, 'r') as f:
        lines = f.readlines()
    with open(database_file, 'w') as f:
        for line in lines:
            if container_id not in line:
                f.write(line)

def get_user_servers(user):
    if not os.path.exists(database_file):
        return []
    servers = []
    with open(database_file, 'r') as f:
        for line in f:
            if line.startswith(user):
                servers.append(line.strip())
    return servers

def count_user_servers(user):
    return len(get_user_servers(user))

def get_all_servers():
    if not os.path.exists(database_file):
        return []
    with open(database_file, 'r') as f:
        return [line.strip() for line in f.readlines()]

def get_container_info(container_id):
    try:
        result = subprocess.run(["docker", "inspect", container_id], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)[0]
    except:
        pass
    return None

def get_container_status(container_id):
    try:
        result = subprocess.run(["docker", "inspect", "--format", "{{.State.Status}}", container_id], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "unknown"

def get_system_resources():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_total = mem.total / (1024 ** 3)
        mem_used = mem.used / (1024 ** 3)
        disk = psutil.disk_usage('/')
        disk_total = disk.total / (1024 ** 3)
        disk_used = disk.used / (1024 ** 3)
        cpu_count = psutil.cpu_count()
        cpu_load = psutil.getloadavg()
        
        # Get network stats
        net_io = psutil.net_io_counters()
        
        # Get process count
        process_count = len(psutil.pids())
        
        return {
            'cpu': cpu_percent,
            'cpu_cores': cpu_count,
            'cpu_load': cpu_load,
            'memory': {'total': round(mem_total, 2), 'used': round(mem_used, 2), 'percent': mem.percent},
            'disk': {'total': round(disk_total, 2), 'used': round(disk_used, 2), 'percent': disk.percent},
            'network': {'sent': net_io.bytes_sent / (1024**3), 'recv': net_io.bytes_recv / (1024**3)},
            'processes': process_count,
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'python_version': platform.python_version()
        }
    except Exception as e:
        print(f"Error getting system resources: {e}")
        return {
            'cpu': 0,
            'cpu_cores': 0,
            'cpu_load': (0, 0, 0),
            'memory': {'total': 0, 'used': 0, 'percent': 0},
            'disk': {'total': 0, 'used': 0, 'percent': 0},
            'network': {'sent': 0, 'recv': 0},
            'processes': 0,
            'hostname': 'unknown',
            'platform': 'unknown',
            'python_version': 'unknown'
        }

def get_resource_color(value):
    if value < 50:
        return SUCCESS_COLOR
    elif value < 80:
        return WARNING_COLOR
    else:
        return ERROR_COLOR

def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

async def capture_ssh_session_line(process):
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output = output.decode('utf-8').strip()
        if "ssh session:" in output:
            return output.split("ssh session:")[1].strip()
    return None

async def send_to_logs(message):
    try:
        for channel_id in LOGS_CHANNEL_IDS:
            channel = bot.get_channel(channel_id)
            if channel:
                perms = channel.permissions_for(channel.guild.me)
                if perms.send_messages:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    await channel.send(f"`[{timestamp}]` {message}")
    except Exception as e:
        print(f"Failed to send logs: {e}")

# ============================================
# UI COMPONENTS
# ============================================

class OSSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=f"{os_data['emoji']} {os_data['name']}", 
                value=os_id, 
                emoji=os_data['emoji'],
                description=os_data['description'][:100]
            )
            for os_id, os_data in OS_OPTIONS.items()
        ]
        super().__init__(
            placeholder="✨ Select your Operating System...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(thinking=True)
            os_id = self.values[0]
            os_data = OS_OPTIONS[os_id]
            await create_server(interaction, os_data["image"], os_data["name"], 
                              os_data["emoji"], os_data["thumbnail"], os_data["color"])
        except Exception as e:
            print(f"Error in OSSelect callback: {e}")
            try:
                await interaction.followup.send("❌ An error occurred while processing your request.", ephemeral=True)
            except:
                pass

class OSView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(OSSelect())

class ManageView(discord.ui.View):
    def __init__(self, container_id, user_id, ssh_command=None, os_name=None):
        super().__init__(timeout=300)
        self.container_id = container_id
        self.user_id = user_id
        self.ssh_command = ssh_command
        self.os_name = os_name
    
    @discord.ui.button(label="🟢 Start", style=discord.ButtonStyle.success, emoji="🟢")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your VPS!", ephemeral=True)
            return
        try:
            subprocess.run(["docker", "start", self.container_id], check=True)
            embed = discord.Embed(
                title="✅ VPS Started", 
                description=f"VPS `{self.container_id[:12]}` has been started on **{NODE_NAME}**!",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await send_to_logs(f"🟢 {interaction.user.mention} started VPS `{self.container_id[:12]}` on {NODE_NAME}")
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=ERROR_COLOR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🛑 Stop", style=discord.ButtonStyle.danger, emoji="🛑")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your VPS!", ephemeral=True)
            return
        try:
            subprocess.run(["docker", "stop", self.container_id], check=True)
            embed = discord.Embed(
                title="✅ VPS Stopped", 
                description=f"VPS `{self.container_id[:12]}` has been stopped!",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await send_to_logs(f"🛑 {interaction.user.mention} stopped VPS `{self.container_id[:12]}` on {NODE_NAME}")
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=ERROR_COLOR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🔄 Restart", style=discord.ButtonStyle.primary, emoji="🔄")
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your VPS!", ephemeral=True)
            return
        try:
            subprocess.run(["docker", "restart", self.container_id], check=True)
            embed = discord.Embed(
                title="✅ VPS Restarted", 
                description=f"VPS `{self.container_id[:12]}` has been restarted!",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await send_to_logs(f"🔄 {interaction.user.mention} restarted VPS `{self.container_id[:12]}` on {NODE_NAME}")
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=ERROR_COLOR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🔑 SSH", style=discord.ButtonStyle.secondary, emoji="🔑")
    async def ssh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your VPS!", ephemeral=True)
            return
        if self.ssh_command:
            embed = discord.Embed(
                title="🔑 SSH Connection Details", 
                description=f"```\n{self.ssh_command}\n```\n\n**Node:** {NODE_NAME}\n**OS:** {self.os_name or 'Unknown'}",
                color=INFO_COLOR
            )
            embed.set_footer(text="Use this command to connect to your VPS")
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("✅ SSH details sent to your DMs!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ SSH command not available.", ephemeral=True)
    
    @discord.ui.button(label="📊 Stats", style=discord.ButtonStyle.secondary, emoji="📊")
    async def stats_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your VPS!", ephemeral=True)
            return
        try:
            result = subprocess.run(["docker", "stats", self.container_id, "--no-stream", "--format", 
                                   "{{.CPUPerc}}|{{.MemUsage}}|{{.NetIO}}|{{.BlockIO}}"], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                stats = result.stdout.strip().split("|")
                embed = discord.Embed(
                    title=f"📊 VPS Stats: `{self.container_id[:12]}`",
                    color=INFO_COLOR
                )
                embed.add_field(name="💻 CPU", value=stats[0] if len(stats) > 0 else "N/A", inline=True)
                embed.add_field(name="🧠 Memory", value=stats[1] if len(stats) > 1 else "N/A", inline=True)
                embed.add_field(name="🌐 Network", value=stats[2] if len(stats) > 2 else "N/A", inline=True)
                embed.add_field(name="💾 Disk I/O", value=stats[3] if len(stats) > 3 else "N/A", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("❌ Could not get stats", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
    
    @discord.ui.button(label="🗑️ Remove", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your VPS!", ephemeral=True)
            return
        
        class ConfirmView(discord.ui.View):
            def __init__(self, container_id, user_id):
                super().__init__(timeout=60)
                self.container_id = container_id
                self.user_id = user_id
            
            @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.danger, emoji="✅")
            async def confirm(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                try:
                    subprocess.run(["docker", "stop", self.container_id], check=False, timeout=10)
                    subprocess.run(["docker", "rm", self.container_id], check=True, timeout=10)
                    remove_from_database(self.container_id)
                    embed = discord.Embed(
                        title="✅ VPS Removed", 
                        description=f"VPS `{self.container_id[:12]}` has been permanently deleted!",
                        color=SUCCESS_COLOR
                    )
                    embed.set_thumbnail(url=SUCCESS_IMAGE)
                    await i.response.edit_message(embed=embed, view=None)
                    await send_to_logs(f"🗑️ {i.user.mention} removed VPS `{self.container_id[:12]}` on {NODE_NAME}")
                except Exception as e:
                    embed = discord.Embed(title="❌ Error", description=str(e), color=ERROR_COLOR)
                    await i.response.edit_message(embed=embed, view=None)
            
            @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
            async def cancel(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                await i.response.edit_message(content="Removal cancelled.", view=None)
        
        embed = discord.Embed(
            title="⚠️ Confirm Removal", 
            description=f"Are you sure you want to remove VPS `{self.container_id[:12]}`?\nThis action cannot be undone!",
            color=WARNING_COLOR
        )
        embed.set_thumbnail(url=WARNING_IMAGE)
        await interaction.response.send_message(embed=embed, view=ConfirmView(self.container_id, self.user_id), ephemeral=True)

# ============================================
# BOT EVENTS
# ============================================

@bot.event
async def on_ready():
    change_status.start()
    cleanup_inactive.start()
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ✨ HK-vi18 VPS Management Bot is Ready! ✨                                 ║
║                                                                              ║
║   🤖 Logged in as: {bot.user}                                                ║
║   🖥️  Node Name: {NODE_NAME}                                                 ║
║   📊 Server Limit: {SERVER_LIMIT} per user                                   ║
║   💾 Database: {database_file}                                               ║
║   🐳 Docker: {'✓' if subprocess.run(['docker', 'ps'], capture_output=True).returncode == 0 else '✗'}               ║
║                                                                              ║
║   💜 Made by AryanDev007                                                     ║
║   🆔 Discord ID: devaru007                                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    try:
        await bot.tree.sync()
        print("✅ Commands synced successfully!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@tasks.loop(minutes=5)
async def cleanup_inactive():
    """Auto-cleanup inactive VPS instances"""
    try:
        if not os.path.exists(database_file):
            return
        
        with open(database_file, 'r') as f:
            lines = f.readlines()
        
        updated_lines = []
        removed_count = 0
        
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) >= 7:
                container_id = parts[1]
                timestamp_str = parts[6]
                
                try:
                    created_at = datetime.fromisoformat(timestamp_str)
                    if datetime.now() - created_at > timedelta(hours=INACTIVE_TIMEOUT_HOURS):
                        # Check if container is still running
                        status = get_container_status(container_id)
                        if status == "exited" or status == "stopped":
                            # Remove inactive container
                            subprocess.run(["docker", "rm", container_id], check=False, timeout=10)
                            removed_count += 1
                            await send_to_logs(f"🧹 Auto-cleaned inactive VPS `{container_id[:12]}`")
                            continue
                except:
                    pass
            
            updated_lines.append(line)
        
        if removed_count > 0:
            with open(database_file, 'w') as f:
                f.writelines(updated_lines)
            print(f"🧹 Cleaned up {removed_count} inactive VPS instances")
            
    except Exception as e:
        print(f"Error in cleanup_inactive: {e}")

@tasks.loop(seconds=5)
async def change_status():
    try:
        instance_count = len(get_all_servers())
        active_count = 0
        for server in get_all_servers():
            parts = server.split('|')
            if len(parts) >= 2:
                status = get_container_status(parts[1])
                if status == "running":
                    active_count += 1
        
        statuses = [  
            f"🌠 {NODE_NAME} | {active_count}/{instance_count} VPS Active",  
            f"⚡ Powering {instance_count} Virtual Servers",  
            f"🔮 {NODE_NAME} Node | {active_count} Running",  
            f"🚀 Hosting {instance_count} VPS Dreams",
            f"💜 Made by Ankit Ex. & PowerDev",
            f"🎯 {NODE_NAME} VPS Management System",
            f"📊 {SERVER_LIMIT} VPS Limit Per User",
            f"🖥️ {len(OS_OPTIONS)} Operating Systems Available"
        ]  
        await bot.change_presence(activity=discord.Game(name=random.choice(statuses)))  
    except Exception as e:  
        print(f"💥 Failed to update status: {e}")

# ============================================
# CORE COMMANDS
# ============================================

@bot.tree.command(name="deploy", description="🚀 Create a new VPS instance on HK-vi18")
async def deploy(interaction: discord.Interaction):
    try:
        if DEPLOY_CHANNEL_IDS and interaction.channel_id not in DEPLOY_CHANNEL_IDS:
            embed = discord.Embed(
                title="🚫 Wrong Channel",
                description=f"Please use this command in designated deploy channels: {', '.join([f'<#{cid}>' for cid in DEPLOY_CHANNEL_IDS])}.",
                color=ERROR_COLOR
            )
            embed.set_image(url=ERROR_IMAGE)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"🚀 {NODE_NAME} VPS Deployment",
            description=f"**Welcome to {NODE_NAME} VPS Management System**\n\n"
                       f"✨ **Select your preferred OS from the menu below:**\n\n"
                       f"**Available Operating Systems:**\n"
                       f"• 🐧 Ubuntu 22.04 LTS - Most popular, beginner friendly\n"
                       f"• 🦕 Debian 12 - Stable and secure\n"
                       f"• ⛰️ Alpine Linux - Lightweight (~5MB)\n"
                       f"• 🎯 Arch Linux - Rolling release\n"
                       f"• 💣 Kali Linux - Security & pentesting\n"
                       f"• 🎩 Fedora 39 - Cutting edge\n"
                       f"• 🟡 CentOS Stream 9 - Enterprise\n"
                       f"• 🪨 Rocky Linux 9 - RHEL compatible\n"
                       f"• 🦌 AlmaLinux 9 - Enterprise ready\n"
                       f"• 🦎 OpenSUSE Leap - User friendly\n\n"
                       f"**Default Specifications:**\n"
                       f"• RAM: {RAM_LIMIT}\n"
                       f"• CPU: {CPU_LIMIT} Cores\n"
                       f"• Storage: {STORAGE_LIMIT}\n"
                       f"• SSH Access: Yes (tmate)\n"
                       f"• Auto-cleanup: After {INACTIVE_TIMEOUT_HOURS} hours of inactivity",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=VPS_MANAGEMENT_IMAGE)
        embed.set_footer(text=f"Node: {NODE_NAME} | Limit: {SERVER_LIMIT} instances | Made with 💜 by Ankit Ex. & PowerDev")
        await interaction.response.send_message(embed=embed, view=OSView())
        
    except Exception as e:
        print(f"Error in deploy command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

async def create_server(interaction, image, os_name, os_emoji, thumbnail, color):
    try:
        user = str(interaction.user)
        
        if count_user_servers(user) >= SERVER_LIMIT:  
            embed = discord.Embed(  
                title="🚫 Limit Reached",  
                description=f"❌ You've reached your limit of {SERVER_LIMIT} VPS instances on {NODE_NAME}!\n\n"
                           f"Please remove some instances before creating new ones.\n"
                           f"Use `/list` to see your instances and `/remove <id>` to delete them.",
                color=ERROR_COLOR  
            )  
            embed.set_thumbnail(url=ERROR_IMAGE)
            try:
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                try:
                    await interaction.channel.send(embed=embed)
                except:
                    pass
            return

        embed = discord.Embed(
            title=f"⚙️ {os_emoji} Creating {os_name} on {NODE_NAME}",
            description=f"```🔮 Preparing your {os_name} experience...\n"
                       f"⏳ This may take 30-60 seconds...\n"
                       f"📦 Image: {image}\n"
                       f"💾 RAM: {RAM_LIMIT}\n"
                       f"⚡ CPU: {CPU_LIMIT} Cores```",
            color=color
        )
        embed.set_thumbnail(url=thumbnail)
        
        try:
            msg = await interaction.followup.send(embed=embed, wait=True)
        except:
            try:
                msg = await interaction.channel.send(embed=embed)
            except Exception as e:
                print(f"Failed to send message: {e}")
                return

        try:  
            container_id = subprocess.check_output([
                "docker", "run", "-itd", "--privileged",
                "--memory", RAM_LIMIT,
                "--cpus", CPU_LIMIT,
                "--name", f"{NODE_NAME.lower()}-{generate_container_id()[:8]}",
                image
            ]).strip().decode('utf-8')  
            await send_to_logs(f"🔧 {interaction.user.mention} deployed {os_emoji} {os_name} on {NODE_NAME} (ID: `{container_id[:12]}`)")
        except subprocess.CalledProcessError as e:  
            embed = discord.Embed(  
                title="❌ Creation Failed",  
                description=f"```🛠️ Error creating container:\n{e}```",  
                color=ERROR_COLOR  
            )  
            embed.set_thumbnail(url=ERROR_IMAGE)
            try:
                await msg.edit(embed=embed)
            except:
                pass
            return  

        try:  
            exec_cmd = await asyncio.create_subprocess_exec(
                "docker", "exec", container_id, "tmate", "-F",  
                stdout=asyncio.subprocess.PIPE, 
                stderr=asyncio.subprocess.PIPE
            )  
            ssh_session_line = await capture_ssh_session_line(exec_cmd)  
            
            if ssh_session_line:  
                dm_embed = discord.Embed(  
                    title=f"🎉 {os_emoji} {os_name} VPS Ready on {NODE_NAME}!",  
                    description=f"**🔑 SSH Command:**\n```{ssh_session_line}```",  
                    color=color  
                )  
                dm_embed.add_field(name="🖥️ Node", value=NODE_NAME, inline=True)
                dm_embed.add_field(name="🖥️ OS", value=os_name, inline=True)  
                dm_embed.add_field(name="🧠 RAM", value=RAM_LIMIT, inline=True)  
                dm_embed.add_field(name="⚡ CPU", value=f"{CPU_LIMIT} Cores", inline=True)
                dm_embed.add_field(name="💾 Storage", value=STORAGE_LIMIT, inline=True)
                dm_embed.add_field(name="🔌 SSH Port", value="22", inline=True)
                dm_embed.add_field(name="📅 Created", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
                dm_embed.set_footer(text=f"💎 This VPS will auto-delete after {INACTIVE_TIMEOUT_HOURS} hours of inactivity\nMade with 💜 by Ankit Ex. & PowerDev")
                dm_embed.set_thumbnail(url=thumbnail)
                
                response_embed = discord.Embed(  
                    title="✅ VPS Deployment Successful!",  
                    description=f"**{os_emoji} {os_name}** VPS created successfully on **{NODE_NAME}**!\n"
                               f"📩 **Check your DMs** for SSH connection details.\n\n"
                               f"**Instance ID:** `{container_id[:12]}`\n"
                               f"**Node:** `{NODE_NAME}`\n"
                               f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    color=SUCCESS_COLOR  
                )  
                response_embed.set_thumbnail(url=VPS_MANAGEMENT_IMAGE)
                
                try:
                    await interaction.user.send(embed=dm_embed)
                except discord.Forbidden:  
                    response_embed.add_field(name="⚠️ DM Failed", 
                                           value="I couldn't DM you. Please enable DMs from server members.\n\n**SSH Command:**\n```" + ssh_session_line + "```", 
                                           inline=False)  
                
                await msg.edit(embed=response_embed)  
                add_to_database(user, container_id, ssh_session_line, None, os_name)  
            else:  
                embed = discord.Embed(  
                    title="❌ SSH Session Failed",  
                    description="Could not establish SSH session. VPS might not be fully ready.",  
                    color=ERROR_COLOR  
                )  
                embed.set_thumbnail(url=ERROR_IMAGE)
                await msg.edit(embed=embed)  
                subprocess.run(["docker", "stop", container_id], check=False)  
                subprocess.run(["docker", "rm", container_id], check=False)  
        except Exception as e:  
            print(f"Error during SSH session creation: {e}")  
            embed = discord.Embed(  
                title="❌ Creation Failed",  
                description=f"```🛠️ An unexpected error occurred during SSH setup:\n{e}```",  
                color=ERROR_COLOR  
            )  
            embed.set_thumbnail(url=ERROR_IMAGE)
            try:
                await msg.edit(embed=embed)
            except:
                pass
            subprocess.run(["docker", "stop", container_id], check=False)  
            subprocess.run(["docker", "rm", container_id], check=False)  

    except Exception as e:
        print(f"Error in create_server: {e}")
        try:
            await interaction.followup.send("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

# ============================================
# MANAGEMENT COMMANDS
# ============================================

@bot.tree.command(name="manage", description="🎛️ Manage your VPS with interactive buttons")
@app_commands.describe(container_id="The ID of the container to manage")
async def manage_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        server_entry = None
        ssh_cmd = None
        os_name = None
        for s in servers:
            if container_id in s:
                server_entry = s
                parts = s.split('|')
                if len(parts) >= 3:
                    ssh_cmd = parts[2]
                if len(parts) >= 6:
                    os_name = parts[5]
                break
        
        if not server_entry:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            embed.set_thumbnail(url=ERROR_IMAGE)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        info = get_container_info(container_id)
        status = get_container_status(container_id)
        
        status_emoji = "🟢" if status == "running" else "🔴" if status == "exited" else "🟡"
        status_text = status.capitalize() if status != "unknown" else "Unknown"
        
        embed = discord.Embed(
            title=f"🎛️ {NODE_NAME} VPS Management Panel",
            description=f"**Instance ID:** `{container_id[:12]}`\n"
                       f"**Status:** {status_emoji} **{status_text}**\n"
                       f"**OS:** {os_name or 'Unknown'}\n"
                       f"**Node:** `{NODE_NAME}`",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=VPS_MANAGEMENT_IMAGE)
        embed.set_footer(text="Use the buttons below to manage your VPS")
        
        view = ManageView(container_id, interaction.user.id, ssh_cmd, os_name)
        await interaction.response.send_message(embed=embed, view=view)
        
    except Exception as e:
        print(f"Error in manage_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="list", description="📜 List your VPS instances on HK-vi18")
async def list_servers(interaction: discord.Interaction):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not servers:
            embed = discord.Embed(
                title=f"📭 No VPS Found on {NODE_NAME}",
                description="You don't have any active VPS instances.\nUse `/deploy` to create one!",
                color=INFO_COLOR
            )
            embed.set_thumbnail(url=VPS_MANAGEMENT_IMAGE)
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title=f"📋 Your VPS Instances on {NODE_NAME} ({len(servers)}/{SERVER_LIMIT})",
            color=EMBED_COLOR
        )
        
        running_count = 0
        for server in servers:
            parts = server.split('|')
            if len(parts) >= 2:
                container_id = parts[1]
                ssh_cmd = parts[2] if len(parts) > 2 else "N/A"
                os_name = parts[5] if len(parts) > 5 else "Unknown"
                
                status = get_container_status(container_id)
                status_emoji = "🟢" if status == "running" else "🔴" if status == "exited" else "🟡"
                
                if status == "running":
                    running_count += 1
                
                # Get OS emoji
                os_emoji = "🖥️"
                for os_id, os_data in OS_OPTIONS.items():
                    if os_data['name'].lower() in os_name.lower():
                        os_emoji = os_data['emoji']
                        break
                
                embed.add_field(
                    name=f"{status_emoji} {os_emoji} {os_name[:30]} - `{container_id[:12]}`",
                    value=f"▫️ Status: {status.capitalize()}\n"
                          f"▫️ Node: {NODE_NAME}\n"
                          f"▫️ RAM: {RAM_LIMIT} | CPU: {CPU_LIMIT} Cores\n"
                          f"▫️ Use `/manage {container_id[:12]}` to control",
                    inline=False
                )
        
        embed.add_field(
            name="📊 Summary",
            value=f"**Total:** {len(servers)} | **Running:** {running_count} | **Stopped:** {len(servers) - running_count}",
            inline=False
        )
        embed.set_thumbnail(url=VPS_MANAGEMENT_IMAGE)
        embed.set_footer(text=f"Made with 💜 by Ankit Ex. & PowerDev | Node: {NODE_NAME}")
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in list_servers: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="start", description="🟢 Start your VPS")
@app_commands.describe(container_id="The ID of the container to start")
async def start_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            subprocess.run(["docker", "start", container_id], check=True)
            embed = discord.Embed(
                title="🟢 VPS Started",
                description=f"VPS `{container_id[:12]}` on **{NODE_NAME}** has been started!",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed)
            await send_to_logs(f"🟢 {interaction.user.mention} started VPS `{container_id[:12]}` on {NODE_NAME}")
        except subprocess.CalledProcessError as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error starting VPS:\n```{e}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in start_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="stop", description="🛑 Stop your VPS")
@app_commands.describe(container_id="The ID of the container to stop")
async def stop_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            subprocess.run(["docker", "stop", container_id], check=True)
            embed = discord.Embed(
                title="🛑 VPS Stopped",
                description=f"VPS `{container_id[:12]}` on **{NODE_NAME}** has been stopped!",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed)
            await send_to_logs(f"🛑 {interaction.user.mention} stopped VPS `{container_id[:12]}` on {NODE_NAME}")
        except subprocess.CalledProcessError as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error stopping VPS:\n```{e}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in stop_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="restart", description="🔄 Restart your VPS")
@app_commands.describe(container_id="The ID of the container to restart")
async def restart_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            subprocess.run(["docker", "restart", container_id], check=True)
            embed = discord.Embed(
                title="🔄 VPS Restarted",
                description=f"VPS `{container_id[:12]}` on **{NODE_NAME}** has been restarted!",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed)
            await send_to_logs(f"🔄 {interaction.user.mention} restarted VPS `{container_id[:12]}` on {NODE_NAME}")
        except subprocess.CalledProcessError as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error restarting VPS:\n```{e}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in restart_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="remove", description="🗑️ Delete your VPS")
@app_commands.describe(container_id="The ID of the container to remove")
async def remove_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:  
            subprocess.run(["docker", "stop", container_id], check=False)  
            subprocess.run(["docker", "rm", container_id], check=True)  
            remove_from_database(container_id)
            
            embed = discord.Embed(  
                title="🗑️ VPS Removed",  
                description=f"VPS `{container_id[:12]}` on **{NODE_NAME}** has been permanently deleted!",
                color=SUCCESS_COLOR  
            )  
            embed.set_thumbnail(url=SUCCESS_IMAGE)
            await interaction.response.send_message(embed=embed)  
            await send_to_logs(f"🗑️ {interaction.user.mention} deleted VPS `{container_id[:12]}` on {NODE_NAME}")
        except subprocess.CalledProcessError as e:  
            embed = discord.Embed(  
                title="❌ Error",  
                description=f"Error removing VPS:\n```{e}```",  
                color=ERROR_COLOR  
            )  
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in remove_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

# ============================================
# STATUS & INFO COMMANDS
# ============================================

@bot.tree.command(name="node", description="📊 View HK-vi18 node statistics and resource usage")
async def node_stats(interaction: discord.Interaction):
    try:
        resources = get_system_resources()
        instance_count = len(get_all_servers())
        active_count = 0
        
        for server in get_all_servers():
            parts = server.split('|')
            if len(parts) >= 2:
                status = get_container_status(parts[1])
                if status == "running":
                    active_count += 1
        
        embed = discord.Embed(
            title=f"📊 {NODE_NAME} Node Statistics",
            description=f"**System Information**\n"
                       f"• Hostname: `{resources['hostname']}`\n"
                       f"• Platform: `{resources['platform']}`\n"
                       f"• Python: `{resources['python_version']}`\n"
                       f"• Node Status: 🟢 **ONLINE**",
            color=NODE_COLOR
        )
        
        # CPU Usage
        cpu_bar = "🟩" * int(resources['cpu']/10) + "⬜" * (10 - int(resources['cpu']/10))
        embed.add_field(
            name="💻 CPU Usage",
            value=f"```yaml\n{resources['cpu']}%\n{cpu_bar}\nCores: {resources['cpu_cores']}\nLoad: {resources['cpu_load'][0]:.2f}, {resources['cpu_load'][1]:.2f}, {resources['cpu_load'][2]:.2f}```",
            inline=False
        )
        
        # Memory Usage
        mem_bar = "🟩" * int(resources['memory']['percent']/10) + "⬜" * (10 - int(resources['memory']['percent']/10))
        embed.add_field(
            name="🧠 Memory Usage",
            value=f"```yaml\n{resources['memory']['used']}GB / {resources['memory']['total']}GB ({resources['memory']['percent']}%)\n{mem_bar}```",
            inline=False
        )
        
        # Disk Usage
        disk_bar = "🟩" * int(resources['disk']['percent']/10) + "⬜" * (10 - int(resources['disk']['percent']/10))
        embed.add_field(
            name="💾 Disk Usage",
            value=f"```yaml\n{resources['disk']['used']}GB / {resources['disk']['total']}GB ({resources['disk']['percent']}%)\n{disk_bar}```",
            inline=False
        )
        
        # Network Stats
        embed.add_field(
            name="🌐 Network Traffic",
            value=f"```yaml\nSent: {resources['network']['sent']:.2f} GB\nReceived: {resources['network']['recv']:.2f} GB```",
            inline=True
        )
        
        # VPS Statistics
        embed.add_field(
            name="📊 VPS Statistics",
            value=f"```yaml\nTotal VPS: {instance_count}\nRunning: {active_count}\nStopped: {instance_count - active_count}\nMax per User: {SERVER_LIMIT}```",
            inline=True
        )
        
        # System Info
        embed.add_field(
            name="⚙️ System Info",
            value=f"```yaml\nProcesses: {resources['processes']}\nUptime: {format_uptime(int(time.time() - psutil.boot_time()))}\nNode: {NODE_NAME}```",
            inline=True
        )
        
        embed.set_thumbnail(url=NODE_STATUS_IMAGE)
        embed.set_footer(text=f"🟩 Healthy | 🟨 Warning | 🟥 Critical\nMade with 💜 by Ankit Ex. & PowerDev")
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in node_stats: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="status", description="🔍 Check the status of your VPS")
@app_commands.describe(container_id="The ID of the container to check status")
async def status_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        status = get_container_status(container_id)
        status_emoji = "🟢" if status == "running" else "🔴" if status == "exited" else "🟡"
        
        # Get more details
        info = get_container_info(container_id)
        created = "Unknown"
        if info:
            created = info.get("Created", "Unknown")[:19].replace("T", " ")
        
        embed = discord.Embed(
            title=f"🔍 VPS Status: `{container_id[:12]}`",
            description=f"**Status:** {status_emoji} **{status.capitalize()}**\n"
                       f"**Node:** **{NODE_NAME}**\n"
                       f"**Created:** {created}",
            color=SUCCESS_COLOR if status == "running" else WARNING_COLOR
        )
        
        if status == "running":
            try:
                stats = subprocess.run(["docker", "stats", container_id, "--no-stream", "--format", 
                                      "{{.CPUPerc}}|{{.MemUsage}}"], capture_output=True, text=True)
                if stats.returncode == 0:
                    parts = stats.stdout.strip().split("|")
                    embed.add_field(name="💻 CPU", value=parts[0] if len(parts) > 0 else "N/A", inline=True)
                    embed.add_field(name="🧠 Memory", value=parts[1] if len(parts) > 1 else "N/A", inline=True)
            except:
                pass
        
        embed.set_thumbnail(url=NODE_STATUS_IMAGE)
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in status_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="stats", description="📈 Get real-time resource usage for your VPS")
@app_commands.describe(container_id="The ID of the container to get stats for")
async def stats_command(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            stats_process = await asyncio.create_subprocess_exec(
                "docker", "stats", container_id, "--no-stream", "--format", 
                "{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}|{{.PIDs}}",
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await stats_process.communicate()

            if stats_process.returncode != 0:
                raise Exception(stderr.decode())

            stats_output = stdout.decode().strip().split("|")
            cpu_usage = stats_output[0] if len(stats_output) > 0 else "N/A"
            mem_usage = stats_output[1] if len(stats_output) > 1 else "N/A"
            mem_perc = stats_output[2] if len(stats_output) > 2 else "N/A"
            net_io = stats_output[3] if len(stats_output) > 3 else "N/A"
            block_io = stats_output[4] if len(stats_output) > 4 else "N/A"
            pids = stats_output[5] if len(stats_output) > 5 else "N/A"

            embed = discord.Embed(
                title=f"📈 VPS Stats: `{container_id[:12]}` on {NODE_NAME}",
                color=INFO_COLOR
            )
            embed.add_field(name="💻 CPU Usage", value=cpu_usage, inline=True)
            embed.add_field(name="🧠 Memory Usage", value=mem_usage, inline=True)
            embed.add_field(name="📊 Memory %", value=mem_perc, inline=True)
            embed.add_field(name="🌐 Network I/O", value=net_io, inline=True)
            embed.add_field(name="💾 Block I/O", value=block_io, inline=True)
            embed.add_field(name="🔢 Processes", value=pids, inline=True)
            embed.set_footer(text="Stats are real-time and may vary.")
            embed.set_thumbnail(url=CPU_IMAGE)
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error Getting Stats",
                description=f"An error occurred: ```{e}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f"Error in stats_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="uptime", description="⏰ Get the uptime of your VPS")
@app_commands.describe(container_id="The ID of the container to check uptime")
async def uptime_command(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        if not any(container_id in s for s in servers):
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            result = subprocess.run(["docker", "inspect", "--format", "{{.State.StartedAt}}", container_id], 
                                  capture_output=True, text=True, check=True)
            started_at_str = result.stdout.strip()
            
            started_at = datetime.strptime(started_at_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
            uptime = datetime.now() - started_at
            
            # Format uptime
            days = uptime.days
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            seconds = uptime.seconds % 60
            
            uptime_str = ""
            if days > 0:
                uptime_str += f"{days}d "
            if hours > 0:
                uptime_str += f"{hours}h "
            if minutes > 0:
                uptime_str += f"{minutes}m "
            uptime_str += f"{seconds}s"

            embed = discord.Embed(
                title=f"⏰ VPS Uptime: `{container_id[:12]}`",
                description=f"**Started:** {started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
                           f"**Uptime:** **{uptime_str}**\n"
                           f"**Node:** **{NODE_NAME}**",
                color=SUCCESS_COLOR
            )
            embed.set_thumbnail(url=NODE_STATUS_IMAGE)
            await interaction.response.send_message(embed=embed)
            
        except subprocess.CalledProcessError as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error getting VPS uptime:\n```{e.stderr}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"An unexpected error occurred: ```{e}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f"Error in uptime_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

# ============================================
# UTILITY COMMANDS
# ============================================

@bot.tree.command(name="ping", description="🏓 Check bot latency")
async def ping_command(interaction: discord.Interaction):
    try:
        latency = round(bot.latency * 1000)
        instance_count = len(get_all_servers())
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"⚡ **Bot Latency:** {latency}ms\n"
                       f"🖥️ **Node:** {NODE_NAME}\n"
                       f"📊 **Active VPS:** {instance_count}\n"
                       f"💜 **Made by:** Ankit Ex. & PowerDev",
            color=SUCCESS_COLOR
        )
        embed.set_thumbnail(url=NODE_STATUS_IMAGE)
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in ping_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="myid", description="🆔 Get your Discord User ID")
async def my_id_command(interaction: discord.Interaction):
    try:
        embed = discord.Embed(
            title="🆔 Your Discord Information",
            description=f"**User ID:** `{interaction.user.id}`\n"
                       f"**Username:** {interaction.user.name}\n"
                       f"**Global Name:** {interaction.user.global_name}\n\n"
                       f"**Node:** {NODE_NAME}\n"
                       f"**Made by:** Ankit Ex. & PowerDev\n"
                       f"**Discord ID:** PowerDev",
            color=INFO_COLOR
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        print(f"Error in my_id_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="info", description="ℹ️ Get detailed information about your VPS")
@app_commands.describe(container_id="The ID of the container to get info")
async def info_server(interaction: discord.Interaction, container_id: str):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)
        
        server_entry = None
        for s in servers:
            if container_id in s:
                server_entry = s
                break
        
        if not server_entry:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not own a VPS with that ID or it does not exist.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        info = get_container_info(container_id)
        if not info:
            embed = discord.Embed(
                title="❌ Error",
                description="Could not get VPS information.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
            return

        status = info.get("State", {}).get("Status", "Unknown")
        created = info.get("Created", "Unknown")[:19].replace("T", " ")
        image = info.get("Config", {}).get("Image", "Unknown")
        
        # Get network info
        networks = info.get("NetworkSettings", {}).get("Networks", {})
        ip_address = "Unknown"
        for net_name, net_info in networks.items():
            ip_address = net_info.get("IPAddress", "Unknown")
            if ip_address != "Unknown":
                break
        
        embed = discord.Embed(
            title=f"ℹ️ VPS Details: `{container_id[:12]}`",
            color=INFO_COLOR
        )
        embed.add_field(name="📦 Image", value=image, inline=True)
        embed.add_field(name="🟢 Status", value=status.capitalize(), inline=True)
        embed.add_field(name="📅 Created", value=created, inline=True)
        embed.add_field(name="🌐 IP Address", value=ip_address, inline=True)
        embed.add_field(name="🖥️ Node", value=NODE_NAME, inline=True)
        embed.add_field(name="💾 RAM", value=RAM_LIMIT, inline=True)
        embed.set_footer(text="Use /stats for real-time resource usage")
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in info_server: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

# ============================================
# BATCH COMMANDS
# ============================================

@bot.tree.command(name="stop_all", description="🛑 Stop all your active VPS instances")
async def stop_all_servers(interaction: discord.Interaction):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)

        if not servers:
            embed = discord.Embed(
                title="📭 No VPS Found",
                description="You don't have any active VPS instances to stop.",
                color=INFO_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        stopped_count = 0
        failed_count = 0
        
        embed = discord.Embed(
            title="🛑 Stopping All VPS",
            description="Processing...",
            color=INFO_COLOR
        )
        await interaction.response.send_message(embed=embed)
        
        for server_entry in servers:
            parts = server_entry.split("|")
            if len(parts) >= 2:
                container_id = parts[1]
                try:
                    subprocess.run(["docker", "stop", container_id], check=True, timeout=10)
                    stopped_count += 1
                    await send_to_logs(f"🛑 {interaction.user.mention} stopped VPS `{container_id[:12]}` on {NODE_NAME}")
                except Exception as e:
                    failed_count += 1
                    await send_to_logs(f"⚠️ Error stopping VPS `{container_id[:12]}`: {e}")

        embed = discord.Embed(
            title="🛑 All VPS Stopped",
            description=f"✅ **Stopped:** {stopped_count}\n"
                       f"❌ **Failed:** {failed_count}\n"
                       f"📊 **Total:** {len(servers)}",
            color=SUCCESS_COLOR if failed_count == 0 else WARNING_COLOR
        )
        embed.set_thumbnail(url=SUCCESS_IMAGE)
        await interaction.edit_original_response(embed=embed)

    except Exception as e:
        print(f"Error in stop_all_servers: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="remove_all", description="🗑️ Remove all your VPS instances")
async def remove_all_servers(interaction: discord.Interaction):
    try:
        user = str(interaction.user)
        servers = get_user_servers(user)

        if not servers:
            embed = discord.Embed(
                title="📭 No VPS Found",
                description="You don't have any VPS instances to remove.",
                color=INFO_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        class ConfirmAllView(discord.ui.View):
            def __init__(self, servers, user_id):
                super().__init__(timeout=60)
                self.servers = servers
                self.user_id = user_id
            
            @discord.ui.button(label="✅ Confirm All", style=discord.ButtonStyle.danger, emoji="✅")
            async def confirm_all(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                
                await i.response.edit_message(content="Processing...", view=None)
                removed_count = 0
                failed_count = 0
                
                for server_entry in self.servers:
                    parts = server_entry.split("|")
                    if len(parts) >= 2:
                        container_id = parts[1]
                        try:
                            subprocess.run(["docker", "stop", container_id], check=False, timeout=10)
                            subprocess.run(["docker", "rm", container_id], check=True, timeout=10)
                            remove_from_database(container_id)
                            removed_count += 1
                            await send_to_logs(f"🗑️ {i.user.mention} removed VPS `{container_id[:12]}` on {NODE_NAME}")
                        except Exception as e:
                            failed_count += 1
                            await send_to_logs(f"⚠️ Error removing VPS `{container_id[:12]}`: {e}")
                
                embed = discord.Embed(
                    title="🗑️ All VPS Removed",
                    description=f"✅ **Removed:** {removed_count}\n"
                               f"❌ **Failed:** {failed_count}\n"
                               f"📊 **Total:** {len(self.servers)}",
                    color=SUCCESS_COLOR if failed_count == 0 else WARNING_COLOR
                )
                embed.set_thumbnail(url=SUCCESS_IMAGE)
                await i.followup.send(embed=embed, ephemeral=True)
            
            @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
            async def cancel(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                await i.response.edit_message(content="Removal cancelled.", view=None)
        
        embed = discord.Embed(
            title="⚠️ Confirm Remove All VPS",
            description=f"Are you sure you want to remove **ALL {len(servers)}** of your VPS instances?\n\n"
                       f"This action cannot be undone!",
            color=WARNING_COLOR
        )
        embed.set_thumbnail(url=WARNING_IMAGE)
        await interaction.response.send_message(embed=embed, view=ConfirmAllView(servers, interaction.user.id), ephemeral=True)

    except Exception as e:
        print(f"Error in remove_all_servers: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

# ============================================
# ADMIN COMMANDS
# ============================================

@bot.tree.command(name="admin_stats", description="📊 Get detailed node statistics (Admin Only)")
async def admin_stats(interaction: discord.Interaction):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        resources = get_system_resources()
        instance_count = len(get_all_servers())
        active_count = 0
        users_count = set()
        
        for server in get_all_servers():
            parts = server.split('|')
            if len(parts) >= 2:
                users_count.add(parts[0])
                status = get_container_status(parts[1])
                if status == "running":
                    active_count += 1
        
        embed = discord.Embed(
            title=f"📊 {NODE_NAME} Admin Statistics",
            color=NODE_COLOR
        )
        
        embed.add_field(name="🖥️ System", 
                       value=f"CPU: {resources['cpu']}%\n"
                             f"RAM: {resources['memory']['used']}GB/{resources['memory']['total']}GB\n"
                             f"Disk: {resources['disk']['used']}GB/{resources['disk']['total']}GB",
                       inline=True)
        
        embed.add_field(name="📊 VPS Stats",
                       value=f"Total VPS: {instance_count}\n"
                             f"Running: {active_count}\n"
                             f"Users: {len(users_count)}",
                       inline=True)
        
        embed.add_field(name="⚙️ Limits",
                       value=f"Max per User: {SERVER_LIMIT}\n"
                             f"RAM per VPS: {RAM_LIMIT}\n"
                             f"CPU per VPS: {CPU_LIMIT}",
                       inline=True)
        
        embed.add_field(name="💾 Database",
                       value=f"File: {database_file}\n"
                             f"Size: {os.path.getsize(database_file) if os.path.exists(database_file) else 0} bytes",
                       inline=True)
        
        embed.add_field(name="🐳 Docker",
                       value=f"Images: {len(subprocess.run(['docker', 'images', '-q'], capture_output=True).stdout.split())}\n"
                             f"Containers: {len(subprocess.run(['docker', 'ps', '-a', '-q'], capture_output=True).stdout.split())}",
                       inline=True)
        
        embed.set_thumbnail(url=NODE_STATUS_IMAGE)
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in admin_stats: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="exec", description="⚙️ Execute a command inside your VPS (Admin Only)")
@app_commands.describe(container_id="The ID of the container", command="The command to execute")
async def exec_command(interaction: discord.Interaction, container_id: str, command: str):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            result = subprocess.run(["docker", "exec", container_id, "sh", "-c", command], 
                                  capture_output=True, text=True, timeout=30)
            
            output = result.stdout
            error = result.stderr
            
            embed = discord.Embed(
                title=f"⚙️ Command Executed on `{container_id[:12]}`",
                color=INFO_COLOR
            )
            
            if output:
                embed.add_field(name="📤 Output", value=f"```bash\n{output[:1000]}\n```", inline=False)
            if error:
                embed.add_field(name="⚠️ Error", value=f"```bash\n{error[:1000]}\n```", inline=False)
            if not output and not error:
                embed.description = "Command executed successfully with no output."
            
            await interaction.response.send_message(embed=embed)
            await send_to_logs(f"⚙️ Admin {interaction.user.mention} executed `{command}` on `{container_id[:12]}`")
            
        except subprocess.TimeoutExpired:
            embed = discord.Embed(
                title="❌ Timeout",
                description="Command execution timed out after 30 seconds.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
        except subprocess.CalledProcessError as e:
            embed = discord.Embed(
                title="❌ Execution Error",
                description=f"```bash\n{e.stderr[:1000]}\n```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
            
    except Exception as e:
        print(f"Error in exec_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="prune", description="🧹 Remove all stopped containers and dangling images (Admin Only)")
async def prune_command(interaction: discord.Interaction):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        class PruneConfirmView(discord.ui.View):
            def __init__(self, user_id):
                super().__init__(timeout=60)
                self.user_id = user_id
            
            @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.danger, emoji="✅")
            async def confirm(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                
                await i.response.edit_message(content="🧹 Pruning Docker system...", view=None)
                
                try:
                    # Prune containers
                    container_result = subprocess.run(["docker", "container", "prune", "-f"], 
                                                    capture_output=True, text=True)
                    # Prune images
                    image_result = subprocess.run(["docker", "image", "prune", "-f"], 
                                                capture_output=True, text=True)
                    # Prune volumes
                    volume_result = subprocess.run(["docker", "volume", "prune", "-f"], 
                                                 capture_output=True, text=True)
                    # Prune networks
                    network_result = subprocess.run(["docker", "network", "prune", "-f"], 
                                                  capture_output=True, text=True)
                    
                    embed = discord.Embed(
                        title="🧹 Docker System Pruned",
                        description="Docker cleanup completed successfully!",
                        color=SUCCESS_COLOR
                    )
                    embed.add_field(name="📦 Containers", value=container_result.stdout.strip() or "No containers pruned", inline=False)
                    embed.add_field(name="🖼️ Images", value=image_result.stdout.strip() or "No images pruned", inline=False)
                    embed.add_field(name="💾 Volumes", value=volume_result.stdout.strip() or "No volumes pruned", inline=False)
                    embed.add_field(name="🌐 Networks", value=network_result.stdout.strip() or "No networks pruned", inline=False)
                    
                    await i.followup.send(embed=embed, ephemeral=True)
                    await send_to_logs(f"🧹 Admin {i.user.mention} pruned Docker system")
                    
                except Exception as e:
                    embed = discord.Embed(
                        title="❌ Prune Error",
                        description=str(e),
                        color=ERROR_COLOR
                    )
                    await i.followup.send(embed=embed, ephemeral=True)
            
            @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
            async def cancel(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                await i.response.edit_message(content="Prune cancelled.", view=None)
        
        embed = discord.Embed(
            title="⚠️ Confirm Docker Prune",
            description="This will remove all stopped containers, dangling images, unused volumes, and unused networks.\n\n"
                       "This action cannot be undone!",
            color=WARNING_COLOR
        )
        await interaction.response.send_message(embed=embed, view=PruneConfirmView(interaction.user.id), ephemeral=True)
        
    except Exception as e:
        print(f"Error in prune_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="broadcast", description="📢 Send a message to all channels (Admin Only)")
@app_commands.describe(message="The message to broadcast")
async def broadcast_command(interaction: discord.Interaction, message: str):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.send_message("📢 Broadcasting message...", ephemeral=True)
        
        sent_count = 0
        failed_count = 0
        
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    perms = channel.permissions_for(guild.me)
                    if perms.send_messages and perms.embed_links:
                        embed = discord.Embed(
                            title=f"📢 {NODE_NAME} Announcement",
                            description=message,
                            color=EMBED_COLOR,
                            timestamp=datetime.now()
                        )
                        embed.set_footer(text=f"Broadcast by {interaction.user.name} | Made by Ankit Ex. & PowerDev")
                        await channel.send(embed=embed)
                        sent_count += 1
                except Exception as e:
                    failed_count += 1
                    print(f"Failed to send to {channel.name}: {e}")
        
        embed = discord.Embed(
            title="✅ Broadcast Complete",
            description=f"✅ **Sent:** {sent_count} channels\n"
                       f"❌ **Failed:** {failed_count} channels",
            color=SUCCESS_COLOR
        )
        await interaction.edit_original_response(embed=embed)
        await send_to_logs(f"📢 Admin {interaction.user.mention} broadcasted a message")
        
    except Exception as e:
        print(f"Error in broadcast_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="set_limit", description="⚙️ Set max VPS per user (Admin Only)")
@app_commands.describe(limit="The new server limit (integer)")
async def set_limit_command(interaction: discord.Interaction, limit: int):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if limit <= 0 or limit > 100:
            embed = discord.Embed(
                title="❌ Invalid Limit",
                description="The server limit must be between 1 and 100.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        global SERVER_LIMIT
        SERVER_LIMIT = limit
        
        # Save to config
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        
        config['server_limit'] = SERVER_LIMIT
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

        embed = discord.Embed(
            title="✅ Server Limit Updated",
            description=f"The maximum number of VPS per user has been set to **{SERVER_LIMIT}**.",
            color=SUCCESS_COLOR
        )
        await interaction.response.send_message(embed=embed)
        await send_to_logs(f"⚙️ Admin {interaction.user.mention} set server limit to {SERVER_LIMIT}")

    except Exception as e:
        print(f"Error in set_limit_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

# ============================================
# HELP COMMAND
# ============================================

@bot.tree.command(name="help", description="ℹ️ Show detailed help message with all commands")
async def help_command(interaction: discord.Interaction):
    try:
        embed = discord.Embed(
            title=f"✨ {NODE_NAME} VPS Management Bot Help",
            description=f"**Welcome to {NODE_NAME} VPS Management System**\n"
                       f"Your one-stop solution for cloud VPS deployment!\n\n"
                       f"**Node Information**\n"
                       f"• Name: {NODE_NAME}\n"
                       f"• Status: 🟢 Online\n"
                       f"• Max Instances per User: {SERVER_LIMIT}\n"
                       f"• Specifications: {RAM_LIMIT} RAM, {CPU_LIMIT} CPU Cores, {STORAGE_LIMIT} Storage\n"
                       f"• Auto-cleanup: After {INACTIVE_TIMEOUT_HOURS} hours of inactivity\n\n"
                       f"**Available Operating Systems:**\n"
                       f"• 🐧 Ubuntu 22.04 LTS - Most popular\n"
                       f"• 🦕 Debian 12 - Stable & secure\n"
                       f"• ⛰️ Alpine Linux - Lightweight\n"
                       f"• 🎯 Arch Linux - Rolling release\n"
                       f"• 💣 Kali Linux - Security tools\n"
                       f"• 🎩 Fedora 39 - Cutting edge\n"
                       f"• 🟡 CentOS Stream 9 - Enterprise\n"
                       f"• 🪨 Rocky Linux 9 - RHEL compatible\n"
                       f"• 🦌 AlmaLinux 9 - Enterprise ready\n"
                       f"• 🦎 OpenSUSE Leap - User friendly",
            color=EMBED_COLOR
        )

        # Core Commands
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            value="**🚀 CORE COMMANDS**",
            inline=False
        )
        
        core_commands = [  
            ("🚀 `/deploy`", "Create a new VPS instance with OS selection menu"),
            ("📜 `/list`", "List all your VPS instances"),
            ("🎛️ `/manage <id>`", "Interactive management panel with buttons"),
            ("📊 `/node`", "Show node statistics and resource usage"),
            ("🔍 `/status <id>`", "Check your VPS status"),
            ("📈 `/stats <id>`", "Get real-time resource usage"),
            ("⏰ `/uptime <id>`", "Get VPS uptime"),
            ("ℹ️ `/info <id>`", "Get detailed VPS information"),
        ]
        
        for cmd, desc in core_commands:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        # Control Commands
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            value="**🎮 CONTROL COMMANDS**",
            inline=False
        )
        
        control_commands = [  
            ("🟢 `/start <id>`", "Start your VPS"),
            ("🛑 `/stop <id>`", "Stop your VPS"),
            ("🔄 `/restart <id>`", "Restart your VPS"),
            ("🗑️ `/remove <id>`", "Delete your VPS"),
            ("🛑 `/stop_all`", "Stop all your VPS instances"),
            ("🗑️ `/remove_all`", "Remove all your VPS instances"),
        ]
        
        for cmd, desc in control_commands:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        # Utility Commands
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            value="**🔧 UTILITY COMMANDS**",
            inline=False
        )
        
        utility_commands = [  
            ("🏓 `/ping`", "Check bot latency"),
            ("🆔 `/myid`", "Get your Discord User ID"),
            ("ℹ️ `/help`", "Show this help message"),
        ]
        
        for cmd, desc in utility_commands:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        # Admin Commands (only show if user is admin)
        if interaction.user.id in ADMIN_IDS:
            embed.add_field(
                name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                value="**👑 ADMIN COMMANDS**",
                inline=False
            )
            
            admin_commands = [  
                ("📊 `/admin_stats`", "Get detailed node statistics"),
                ("⚙️ `/exec <id> <command>`", "Execute command inside VPS"),
                ("🧹 `/prune`", "Clean Docker system"),
                ("📢 `/broadcast <message>`", "Broadcast message to all channels"),
                ("⚙️ `/set_limit <limit>`", "Set max VPS per user"),
                ("🗑️ `/clear_all`", "Clear all VPS instances"),
                ("📦 `/pull_image <name>`", "Pull Docker image"),
                ("🖼️ `/list_images`", "List Docker images"),
                ("✉️ `/send_dm <id> <msg>`", "Send DM to user"),
                ("➕ `/add_admin <id>`", "Add admin user"),
                ("➖ `/remove_admin <id>`", "Remove admin user"),
            ]
            
            for cmd, desc in admin_commands:
                embed.add_field(name=cmd, value=desc, inline=False)
        
        embed.set_thumbnail(url=HELP_BANNER)
        embed.set_footer(text=f"💜 Made by Ankit Ex. & PowerDev | Discord ID: PowerDev\n💡 Deploy in: {', '.join([f'<#{cid}>' for cid in DEPLOY_CHANNEL_IDS]) if DEPLOY_CHANNEL_IDS else 'Any channel'}")
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"Error in help_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred while processing your request.", ephemeral=True)
        except:
            pass

# ============================================
# ADDITIONAL ADMIN COMMANDS
# ============================================

@bot.tree.command(name="clear_all", description="⚠️ Clear all VPS instances (Admin Only)")
async def clear_all_command(interaction: discord.Interaction):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        class ClearAllView(discord.ui.View):
            def __init__(self, user_id):
                super().__init__(timeout=60)
                self.user_id = user_id
            
            @discord.ui.button(label="⚠️ Confirm Clear All", style=discord.ButtonStyle.danger, emoji="⚠️")
            async def confirm(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                
                await i.response.edit_message(content="🧹 Clearing all VPS instances...", view=None)
                
                try:
                    removed_count = 0
                    failed_count = 0
                    
                    # Get all container IDs from database
                    for server in get_all_servers():
                        parts = server.split('|')
                        if len(parts) >= 2:
                            container_id = parts[1]
                            try:
                                subprocess.run(["docker", "stop", container_id], check=False, timeout=10)
                                subprocess.run(["docker", "rm", container_id], check=True, timeout=10)
                                removed_count += 1
                            except Exception as e:
                                failed_count += 1
                                print(f"Error removing {container_id}: {e}")
                    
                    # Clear database
                    if os.path.exists(database_file):
                        os.remove(database_file)
                        open(database_file, 'w').close()
                    
                    embed = discord.Embed(
                        title="✅ All VPS Cleared",
                        description=f"✅ **Removed:** {removed_count}\n"
                                   f"❌ **Failed:** {failed_count}\n"
                                   f"📊 **Total processed:** {removed_count + failed_count}",
                        color=SUCCESS_COLOR
                    )
                    await i.followup.send(embed=embed, ephemeral=True)
                    await send_to_logs(f"⚠️ Admin {i.user.mention} cleared all VPS instances")
                    
                except Exception as e:
                    embed = discord.Embed(
                        title="❌ Error",
                        description=str(e),
                        color=ERROR_COLOR
                    )
                    await i.followup.send(embed=embed, ephemeral=True)
            
            @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
            async def cancel(self, i: discord.Interaction, b: discord.ui.Button):
                if i.user.id != self.user_id:
                    await i.response.send_message("❌ Unauthorized!", ephemeral=True)
                    return
                await i.response.edit_message(content="Clear all cancelled.", view=None)
        
        instance_count = len(get_all_servers())
        embed = discord.Embed(
            title="⚠️ Confirm Clear All VPS",
            description=f"This will remove **ALL {instance_count}** VPS instances from the system.\n\n"
                       f"This action cannot be undone!",
            color=WARNING_COLOR
        )
        await interaction.response.send_message(embed=embed, view=ClearAllView(interaction.user.id), ephemeral=True)
        
    except Exception as e:
        print(f"Error in clear_all_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="pull_image", description="⬇️ Pull a Docker image (Admin Only)")
@app_commands.describe(image_name="The name of the Docker image to pull")
async def pull_image_command(interaction: discord.Interaction, image_name: str):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"⬇️ Pulling Image: `{image_name}`",
            description="This may take a moment...",
            color=INFO_COLOR
        )
        await interaction.response.send_message(embed=embed)

        try:
            pull_process = await asyncio.create_subprocess_exec(
                "docker", "pull", image_name,
                stdout=asyncio.subprocess.PIPE, 
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await pull_process.communicate()

            if pull_process.returncode != 0:
                raise Exception(stderr.decode())

            embed = discord.Embed(
                title=f"✅ Image Pulled: `{image_name}`",
                description=f"```\n{stdout.decode()[-500:]}\n```" if stdout else "Image pulled successfully!",
                color=SUCCESS_COLOR
            )
            await interaction.edit_original_response(embed=embed)
            await send_to_logs(f"⬇️ Admin {interaction.user.mention} pulled Docker image `{image_name}`")
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error Pulling Image",
                description=f"```{e}```",
                color=ERROR_COLOR
            )
            await interaction.edit_original_response(embed=embed)

    except Exception as e:
        print(f"Error in pull_image_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="list_images", description="🖼️ List all available Docker images (Admin Only)")
async def list_images_command(interaction: discord.Interaction):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            result = subprocess.run(["docker", "images", "--format", "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"], 
                                  capture_output=True, text=True, check=True)
            images_output = result.stdout

            embed = discord.Embed(
                title="🖼️ Docker Images",
                description=f"```\n{images_output[:1900]}\n```" if images_output else "No Docker images found.",
                color=INFO_COLOR
            )
            await interaction.response.send_message(embed=embed)
            await send_to_logs(f"🖼️ Admin {interaction.user.mention} listed Docker images")
            
        except subprocess.CalledProcessError as e:
            embed = discord.Embed(
                title="❌ Error Listing Images",
                description=f"```{e.stderr}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed)
            
    except Exception as e:
        print(f"Error in list_images_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="send_dm", description="✉️ Send a DM to a user (Admin Only)")
@app_commands.describe(user_id="The ID of the user", message="The message to send")
async def send_dm_command(interaction: discord.Interaction, user_id: str, message: str):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            user = await bot.fetch_user(int(user_id))
            if user:
                dm_embed = discord.Embed(
                    title=f"✉️ Message from {NODE_NAME} Admin",
                    description=message,
                    color=EMBED_COLOR,
                    timestamp=datetime.now()
                )
                dm_embed.set_footer(text=f"Sent by {interaction.user.name}")
                await user.send(embed=dm_embed)
                
                embed = discord.Embed(
                    title="✅ DM Sent",
                    description=f"Message successfully sent to <@{user_id}>.",
                    color=SUCCESS_COLOR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await send_to_logs(f"✉️ Admin {interaction.user.mention} sent DM to <@{user_id}>")
            else:
                embed = discord.Embed(
                    title="❌ User Not Found",
                    description="Could not find a user with that ID.",
                    color=ERROR_COLOR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error Sending DM",
                description=f"```{e}```",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        print(f"Error in send_dm_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="add_admin", description="➕ Add a user to admin list (Admin Only)")
@app_commands.describe(user_id="The ID of the user to add as admin")
async def add_admin_command(interaction: discord.Interaction, user_id: str):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            user_id_int = int(user_id)
            if user_id_int not in ADMIN_IDS:
                ADMIN_IDS.append(user_id_int)
                
                # Save to config
                config = {}
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                
                config['admin_ids'] = ADMIN_IDS
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)
                
                embed = discord.Embed(
                    title="✅ Admin Added",
                    description=f"User <@{user_id_int}> has been added to the admin list.",
                    color=SUCCESS_COLOR
                )
                await interaction.response.send_message(embed=embed)
                await send_to_logs(f"➕ Admin {interaction.user.mention} added <@{user_id_int}> to admin list")
            else:
                embed = discord.Embed(
                    title="ℹ️ Already Admin",
                    description=f"User <@{user_id_int}> is already an admin.",
                    color=INFO_COLOR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid User ID",
                description="Please provide a valid integer for the user ID.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        print(f"Error in add_admin_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

@bot.tree.command(name="remove_admin", description="➖ Remove a user from admin list (Admin Only)")
@app_commands.describe(user_id="The ID of the user to remove from admin")
async def remove_admin_command(interaction: discord.Interaction, user_id: str):
    try:
        if interaction.user.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="🚫 Unauthorized",
                description="You do not have permission to use this command.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            user_id_int = int(user_id)
            if user_id_int in ADMIN_IDS:
                ADMIN_IDS.remove(user_id_int)
                
                # Save to config
                config = {}
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                
                config['admin_ids'] = ADMIN_IDS
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)
                
                embed = discord.Embed(
                    title="✅ Admin Removed",
                    description=f"User <@{user_id_int}> has been removed from the admin list.",
                    color=SUCCESS_COLOR
                )
                await interaction.response.send_message(embed=embed)
                await send_to_logs(f"➖ Admin {interaction.user.mention} removed <@{user_id_int}> from admin list")
            else:
                embed = discord.Embed(
                    title="ℹ️ Not Admin",
                    description=f"User <@{user_id_int}> is not in the admin list.",
                    color=INFO_COLOR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid User ID",
                description="Please provide a valid integer for the user ID.",
                color=ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        print(f"Error in remove_admin_command: {e}")
        try:
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        except:
            pass

# ============================================
# RUN BOT
# ============================================

if __name__ == "__main__":
    # Load config if exists
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if 'server_limit' in config:
                    SERVER_LIMIT = config['server_limit']
                if 'admin_ids' in config:
                    ADMIN_IDS = config['admin_ids']
        except:
            pass
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🚀 Starting {NODE_NAME} VPS Management Bot...                               ║
║                                                                              ║
║   📊 Configuration:                                                          ║
║   • Node Name: {NODE_NAME}                                                   ║
║   • Server Limit: {SERVER_LIMIT} per user                                    ║
║   • RAM Limit: {RAM_LIMIT} per VPS                                           ║
║   • CPU Limit: {CPU_LIMIT} cores per VPS                                     ║
║   • Storage Limit: {STORAGE_LIMIT} per VPS                                   ║
║   • Admin Count: {len(ADMIN_IDS)}                                            ║
║   • Deploy Channels: {len(DEPLOY_CHANNEL_IDS)}                               ║
║   • Log Channels: {len(LOGS_CHANNEL_IDS)}                                    ║
║                                                                              ║
║   💜 Made by AryanDev007                                                    ║
║   🆔 Discord ID: devaru007                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    bot.run(TOKEN)
