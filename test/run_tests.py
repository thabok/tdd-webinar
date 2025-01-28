import os
from datetime import datetime

from btc_embedded import EPRestApi, get_merged_config, util

# expect epp file matching the mdl/slx file name the 'model' directory
work_dir = os.path.abspath('test')
epp_file = os.path.join(work_dir, 'seat_heating_control_converted.epp')
project_name = os.path.basename(epp_file)[:-7]

# BTC EmbeddedPlatform API object
ep = EPRestApi(config=get_merged_config())

# Load a BTC EmbeddedPlatform profile (*.epp) and update it
ep.get(f'profiles/{epp_file}', message="Loading profile")
ep.put('architectures?performUpdateCheck=true', message="Updating model & generating code")

# Execute requirements-based tests
exec_start_time = datetime.now()
scopes = ep.get('scopes')
scope_uids = [scope['uid'] for scope in scopes]
toplevel_scope_uid = scope_uids[0]
rbt_exec_payload = {
    'UIDs': scope_uids,
   'data' : { 'execConfigNames' : [ 'SL MIL', 'SIL' ] }
}
rbt_response = ep.post('scopes/test-execution-rbt', rbt_exec_payload, message="Running requirements-based tests")
util.print_rbt_results(rbt_response)
test_cases = ep.get('test-cases-rbt')

# B2B test (with automatic test generation for full MCDC coverage)
vector_gen_settings = {
    'scopeUid'  : toplevel_scope_uid,
    'pllString' : 'MCDC' 
}
ep.post('coverage-generation', vector_gen_settings, message="Generating vectors for structural coverage")
b2b_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-b2b")

# B2B MIL vs. SIL execution
b2b_response = ep.post(f"scopes/{toplevel_scope_uid}/b2b", { 'refMode': 'SL MIL', 'compMode': 'SIL' }, message="Running B2B test")
util.print_b2b_results(b2b_response, b2b_coverage)

# Create project report
report = ep.post(f"scopes/{toplevel_scope_uid}/project-report", message="Creating test report")
# export project report to a file called 'report.html'
report_dir = os.path.abspath('reports')
ep.post(f"reports/{report['uid']}", { 'exportPath': report_dir, 'newName': 'report' })
# Dump JUnit XML report
util.dump_testresults_junitxml(
    b2b_result=b2b_response,
    rbt_results=rbt_response,
    scopes=scopes,
    test_cases=test_cases,
    start_time=exec_start_time,
    project_name=project_name,
    output_file=os.path.join(report_dir, 'test_results.xml')
)

# Save *.epp
ep.put('profiles', { 'path': epp_file }, message="Saving profile")

print('Finished with workflow and create a test report here: ' + report_dir)
