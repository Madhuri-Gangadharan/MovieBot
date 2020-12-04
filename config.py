
import watson_developer_cloud
from slackclient import  SlackClient
location = "/Users/madhuri/Documents/MS/Fall-2020/IS/Movie-Recommendation-Chatbot/"  

# Slack configuration: Slack bot token and verification token is fetched

SLACK_BOT_TOKEN='xoxb-1537693727958-1551909119252-uGdlSMXQKQHRIoU17qeONWfK'
SLACK_VERIFICATION_TOKEN='xDzOxKYl6jHqHLFwBCiXt5TL'

# instantiate slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

#watson configuration : api key and workspace id is fetched
service = watson_developer_cloud.AssistantV1(
    iam_apikey = '5Xb0ruZusvZRX3-Rpyl3RZ2gEoMttuhrclh_axWS_LGz',
    version = '2018-09-20'
)

workspace_id = 'c3fbbdf0-5e17-4531-9dae-b72bd8f92631'

onetime_path = location + "nlp/nlp_solutions/onetime.txt.py"
onetime_file = location + "nlp/nlp_solutions/onetime.txt"
