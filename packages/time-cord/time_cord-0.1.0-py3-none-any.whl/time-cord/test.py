from insights import TCInsights

tc = TCInsights()

print(tc.log_data(lvl="server", scope="last 50 weeks", fuzz=301, nice=True))
