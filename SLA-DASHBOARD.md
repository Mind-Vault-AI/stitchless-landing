# SLA Dashboard - Truth Searcher System

**Last Updated:** *Automatically updated by SLA Monitoring workflow*

## 🎯 SLA Targets

| Metric | Target | Status |
|--------|--------|--------|
| System Uptime | 99.9% | 🔄 Monitoring |
| Response Time (95th percentile) | <2000ms | 🔄 Monitoring |
| Error Rate | <0.1% | 🔄 Monitoring |
| Max Downtime (per month) | 43.8 minutes | 🔄 Monitoring |

## 📊 Current Metrics

### Uptime Statistics

| Period | Uptime % | Downtime (minutes) |
|--------|----------|-------------------|
| Last Hour | N/A | - |
| Last 24 Hours | N/A | - |
| Last 7 Days | N/A | - |
| Last 30 Days | N/A | - |

*Metrics will be populated after the first health checks complete.*

### Performance Metrics

| Metric | Current Value | Target |
|--------|--------------|---------|
| Average Response Time | N/A | <2000ms |
| Health Check Interval | 5 minutes | 5 minutes |
| Alert Threshold | 2 consecutive failures | 2 consecutive failures |

## 🔍 Monitored Services

- ✅ **OpenAI API** - Primary AI service for analysis
- ✅ **SerpAPI** - Primary search provider (optional)
- ✅ **DuckDuckGo** - Fallback search provider
- ✅ **Application Core** - Core application modules

## 📈 Health Status Legend

- **Healthy** (🟢): All systems operational
- **Degraded** (🟡): Non-critical services affected, fallbacks active
- **Unhealthy** (🔴): Critical services down, manual intervention required

## 🚨 Recent Incidents

See [Issues with label: health-alert](../../issues?q=is%3Aissue+label%3Ahealth-alert)

## 📋 Monitoring Details

- **Monitoring Frequency:** Every 5 minutes
- **Data Retention:** 30 days
- **Alert Method:** GitHub Issues + Workflow failures
- **Recovery:** Automated monitoring, manual intervention for critical failures

## 🔗 Quick Links

- [Health Check Workflow](../../actions/workflows/health-check.yml)
- [SLA Monitoring Workflow](../../actions/workflows/sla-monitoring.yml)
- [Monitoring Documentation](./MONITORING.md)
- [Health Check Metrics](.github/metrics/health_checks.csv)

---

*This dashboard is automatically updated by the SLA Monitoring workflow.*
