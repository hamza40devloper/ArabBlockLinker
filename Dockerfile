# Use Java 21 LTS which is perfectly stable and optimized for Minecraft 1.21.11
FROM itzg/minecraft-server:java21

# Accept the Minecraft End User License Agreement (EULA)
ENV EULA=TRUE

# Use PaperMC engine for best performance and lag reduction in SMP servers
ENV TYPE=PAPER

# Strictly lock the Minecraft server version to 1.21.11
ENV VERSION=1.21.11

# Set the Server Message of the Day (MOTD) with custom colors
ENV MOTD="§6§lNovaSMP §7- §bOfficial 1.21.11 Survival"

# Expose the default Minecraft Java Edition port
EXPOSE 25565
