SHELL := /bin/bash
.PHONY: ps clean update build start stop deploy reload help

help:
	@echo ""
	@echo "🛠️  Pieejamās Make komandas:"
	@echo ""
	@echo "  make ps        # Display running Docker containers"
	@echo "  make clean		  # Tīra docker konteinerus un attēlus"
	@echo "  make update 		# Force-pull izmaiņas no git"
	@echo "  make build 		# Izveido Docker konteinerus"
	@echo "  make start     # Build and start Docker containers"
	@echo "  make stop			# Stop and remove Docker containers"
	@echo "  make deploy		# Pilns deploy: stop → update → start"
	@echo "  make reload  	# Stop and start Docker containers"
	@echo ""

ps:
	@echo "📦 Docker konteineru saraksts"
	@docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}" -a

clean:
	@echo "🧹 Tīra docker konteinerus un attēlus"
	@docker system prune -f --volumes

# Force-pull izmaiņas no git
update:
	@bash ./scripts/git-pull-from-repo.bash
	@echo "✅ Git repository force updated from origin/main"

# Build Docker konteinerus
build:
	@docker compose --build
	@echo "🚀 Docker containers built"

# Start Docker konteinerus
start:
	@docker compose up -d
	@echo "🚀 Docker containers started"

# Stop + remove Docker konteinerus
stop:
	@docker compose down
	@echo "🛑 Docker containers stopped and removed"

# Pilns deploy: stop → update → start
deploy: stop clean update build start ps
	@echo "🎉 Deployment completed"

reload: stop start ps
	@echo "🔄 Reload completed"
