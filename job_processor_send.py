import requests

job = {
    'ip_port': '127.0.0.1:999',
    'scan_type': 'Is-Alive',
    'report_id': '4',
}
job_endpoint_of_flask_scanningnode = f'http://127.0.0.1:5000'  # depends on container
res = requests.post(job_endpoint_of_flask_scanningnode, json=job)