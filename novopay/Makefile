# Discoverable agent/developer entrypoints for this monorepo workspace.
.PHONY: help validate lint format

SERVICE ?=
ARGS ?=

help:
	@echo "Novopay workspace targets"
	@echo "  make validate SERVICE=<dir>   Compile/check a service (Gradle or Node)"
	@echo "  make validate SERVICE=<dir> TEST=1   Also run unit tests when supported"
	@echo "  make lint SERVICE=<dir>       Lint/format-check when the service has tooling"
	@echo "  make format SERVICE=<dir>     Format when the service has tooling"
	@echo ""
	@echo "Examples:"
	@echo "  make validate SERVICE=novopay-platform-api-gateway"
	@echo "  make lint SERVICE=novopay-platform-webapp"
	@echo "E2E proof (only when asked): bob validate-ticket <id>"

validate:
	@python scripts/validate-change.py $(SERVICE) $(ARGS) $(if $(TEST),--test,)

lint:
	@python scripts/validate-change.py --lint $(SERVICE) $(ARGS)

format:
	@python scripts/validate-change.py --format $(SERVICE) $(ARGS)
