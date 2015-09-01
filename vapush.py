import sys
import os

import paramiko, scp
import tempfile 

def push(infile, outfile, keypath, host="192.168.115.17", username="lasradm", basedir="/opt/sas/config/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad"):

    key = paramiko.RSAKey.from_private_key_file(keypath)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.load_system_host_keys()
    client.connect(host, username=username, pkey=key)

    transport = client.get_transport()

    scpclient = scp.SCPClient(transport)

    if outfile.startswith("/"):
        outpath = outfile
    else:
        outpath = os.path.join(basedir, "Append", outfile)
    
    scpclient.put(infile, outpath)
    
def push_df(df, outfile, *args, **kwargs):

    pd = df.toPandas()
    t = tempfile.mktemp()
    pd.to_csv(t, index=False, encoding="utf8", date_format="%Y-%m-%dT%H:%M")
    
    push(t, outfile, *args, **kwargs)
