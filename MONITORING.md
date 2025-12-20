# Monitoring Documentation - Truth Searcher System

## Overview

The Truth Searcher system implements comprehensive monitoring and health checking to achieve a 99.9% SLA (Service Level Agreement). This document describes the monitoring architecture, alert procedures, and recovery mechanisms.

## SLA Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **System Uptime** | 99.9% | Monthly uptime percentage |
| **Max Downtime** | 43.8 minutes/month | Cumulative downtime in rolling 30-day window |
| **Response Time** | <2000ms (95th percentile) | Average response time across all health checks |
| **Error Rate** | <0.1% | Percentage of failed requests |
| **Monitoring Interval** | 5 minutes | Frequency of automated health checks |
| **Alert Threshold** | 2 consecutive failures | Trigger for automated alerts |

## Architecture

### Health Check System

The health check system is implemented in `truth-searcher/health_check.py` and monitors:

1. **Application Core**
   - Module imports and initialization
   - Configuration loading
   - Basic functionality

2. **OpenAI API** (Critical)
   - API key configuration
   - API connectivity
   - Response time
   - Token usage

3. **SerpAPI** (Optional)
   - API key configuration (if provided)
   - Search functionality
   - Response time
   - Falls back to DuckDuckGo if unavailable

4. **DuckDuckGo Search** (Fallback)
   - Search functionality
   - Response time
   - No authentication required

### Health Status Levels

- **Healthy** 🟢: All systems operational, all checks passed
- **Degraded** 🟡: Non-critical services affected (e.g., SerpAPI down, DuckDuckGo working)
- **Unhealthy** 🔴: Critical services down (e.g., OpenAI API or Application Core failed)

### Health Check Endpoint

Access the health check endpoint via:
- **URL:** `http://localhost:8501/?health=true` (when running locally)
- **Alternative:** `http://localhost:8501/?mode=health`

The endpoint returns:
- Visual dashboard with service status
- JSON output with detailed metrics
- Response times for each service
- Overall system health status

## GitHub Actions Workflows

### 1. Health Check Monitoring (`health-check.yml`)

**Triggers:**
- Every 5 minutes (scheduled)
- On push to main branch (truth-searcher code changes)
- Manual workflow dispatch

**Process:**
1. Checkout repository
2. Setup Python environment
3. Install dependencies
4. Run health checks with API keys from secrets
5. Store results in `.github/metrics/health_checks.csv`
6. Commit metrics to repository
7. Check for consecutive failures
8. Create GitHub issue if 2+ consecutive failures
9. Fail workflow if status is "unhealthy"

**Secrets Required:**
- `OPENAI_API_KEY` - Required for core functionality
- `SERPAPI_KEY` - Optional, improves search quality

### 2. SLA Monitoring & Reporting (`sla-monitoring.yml`)

**Triggers:**
- Every hour (scheduled)
- After health check workflow completes
- Manual workflow dispatch

**Process:**
1. Checkout repository with full history
2. Calculate SLA metrics from health check data
3. Compute uptime percentages for:
   - Last hour
   - Last 24 hours
   - Last 7 days
   - Last 30 days
4. Update `SLA-DASHBOARD.md` with current metrics
5. Commit updated dashboard
6. Check SLA compliance
7. Create GitHub issue if SLA target not met (<99.9%)

## Metrics Storage

### Health Check Metrics (`/.github/metrics/health_checks.csv`)

Format: `timestamp,status,response_time_ms`

Example:
```csv
2024-01-15T10:30:00Z,healthy,245.67
2024-01-15T10:35:00Z,healthy,198.32
2024-01-15T10:40:00Z,degraded,532.11
```

**Data Retention:** 30 days (8,640 entries at 5-minute intervals)

## Alert System

### Alert Types

1. **Health Alert** (Label: `health-alert`)
   - Triggered by: 2 consecutive unhealthy checks
   - Severity: Urgent
   - Auto-created: Yes
   - Auto-closed: No (requires manual review)

2. **SLA Violation Alert** (Label: `sla-violation`)
   - Triggered by: 30-day uptime < 99.9%
   - Severity: Urgent
   - Auto-created: Yes
   - Auto-closed: No (requires manual review)

### Alert Content

Health alerts include:
- Current system status
- Timestamp of failure
- Average response time
- Action items for investigation
- SLA impact assessment

SLA violation alerts include:
- 30-day uptime percentage
- Total downtime in minutes
- Recent performance trends
- Required corrective actions
- Link to SLA dashboard

### Alert Deduplication

- Only one alert issue per type is created
- Existing open alerts are not duplicated
- Closed alerts can be reopened if issue recurs

## Recovery Procedures

### Automated Recovery

1. **Fallback Services**
   - SerpAPI failure → Automatic DuckDuckGo fallback
   - No manual intervention required

2. **Monitoring Continuity**
   - Health checks continue during degraded state
   - Metrics collection unaffected
   - Alerts accumulate for pattern analysis

### Manual Recovery

When alerts are triggered:

1. **Immediate Response (< 5 minutes)**
   - Check GitHub Actions logs for error details
   - Review health check workflow run
   - Verify API keys in repository secrets

2. **Investigation (< 15 minutes)**
   - Check external service status pages:
     - OpenAI: https://status.openai.com/
     - SerpAPI: https://serpapi.com/status
   - Review recent code changes
   - Check for quota/rate limit issues

3. **Resolution (< 30 minutes)**
   - Fix configuration issues
   - Update API keys if expired
   - Deploy fixes or rollback changes
   - Document incident in GitHub issue

4. **Post-Incident**
   - Update monitoring thresholds if needed
   - Improve alert procedures
   - Add preventive checks
   - Update documentation

## Testing Health Checks

### Local Testing

```bash
# Navigate to truth-searcher directory
cd truth-searcher

# Set environment variables
export OPENAI_API_KEY="your-key-here"
export SERPAPI_KEY="your-key-here"  # optional

# Run health check directly
python health_check.py

# Run via Streamlit app
streamlit run app.py
# Then visit: http://localhost:8501/?health=true
```

### Manual Workflow Testing

1. Go to Actions tab in GitHub
2. Select "Health Check Monitoring" workflow
3. Click "Run workflow"
4. Select branch
5. Review results

## Monitoring Best Practices

### Do's ✅

- Monitor all critical dependencies
- Keep health checks lightweight and fast
- Use appropriate timeouts
- Log detailed error information
- Maintain metric history
- Review alerts promptly
- Document incidents
- Update procedures based on learnings

### Don'ts ❌

- Don't make expensive API calls in health checks
- Don't ignore degraded states
- Don't disable monitoring during issues
- Don't rely on single point of failure
- Don't skip post-incident reviews

## Dashboard Access

- **SLA Dashboard:** [SLA-DASHBOARD.md](./SLA-DASHBOARD.md)
- **Workflow Runs:** [GitHub Actions](../../actions)
- **Health Alerts:** [Open Issues](../../issues?q=is%3Aopen+label%3Ahealth-alert)
- **Metrics Data:** [Health Check CSV](.github/metrics/health_checks.csv)

## Configuration

### Adjusting Monitoring Frequency

Edit `.github/workflows/health-check.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Change '5' to desired interval
```

### Adjusting Alert Threshold

Edit `.github/workflows/health-check.yml`:

```yaml
if: steps.check_failures.outputs.consecutive_failures >= 2  # Change '2' to desired threshold
```

### Adding New Service Checks

1. Add check method to `health_check.py`:
   ```python
   def check_new_service(self) -> HealthCheckResult:
       # Implementation
   ```

2. Add to `run_all_checks()`:
   ```python
   self.checks.append(self.check_new_service())
   ```

3. Update documentation

## Troubleshooting

### Health Checks Always Failing

**Possible Causes:**
- Missing or invalid API keys
- Network connectivity issues
- Rate limiting
- Service outages

**Solutions:**
1. Verify secrets in repository settings
2. Check external service status
3. Review rate limits and quotas
4. Check GitHub Actions network policies

### Metrics Not Updating

**Possible Causes:**
- Git push failures
- Permission issues
- Workflow disabled

**Solutions:**
1. Check workflow runs for errors
2. Verify repository write permissions
3. Ensure workflows are enabled
4. Check branch protection rules

### False Positive Alerts

**Possible Causes:**
- Network transient issues
- Service temporary unavailability
- Timeout too aggressive

**Solutions:**
1. Increase alert threshold (>2 failures)
2. Adjust timeout values
3. Implement retry logic
4. Add grace period for degraded state

## Support

For issues or questions:
1. Check [GitHub Issues](../../issues)
2. Review [SLA Dashboard](./SLA-DASHBOARD.md)
3. Examine workflow logs
4. Create new issue with `monitoring` label

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Maintained By:** Truth Searcher Team
