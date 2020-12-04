import time
import datetime
from slack_files.slack_commands import parse_bot_commands,output_command
from config import slack_client
from nlp.nlp_commands import handle_command
import pandas as pd
import json

user_input = ''
context = {}
current_action = ''
follow_ind = 0

#stores the details of user
session_df = pd.DataFrame({},columns=['timestamp', 'user', 'context'])

bot_id = None
RTM_READ_DELAY = 1

# My program starts running here
if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("MovieBot connected and running!")
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            user_id,message_user,message,team,channel,start_timestamp  = parse_bot_commands(slack_client.rtm_read(),bot_id) #slack processing
            # If there is a message in Slack
            if message:
                try:
                    context = json.loads(session_df.loc[session_df.user == message_user+channel,'context'].values[0])
                except:
                    context = {}
                    session_df = session_df.append({'timestamp': start_timestamp, 'user': message_user+channel, 'context': json.dumps(context)}, ignore_index=True)
                #nlp processing is done here
                context,slack_output,current_action = handle_command(message,channel, message_user,context)
                session_df.loc[session_df.user == message_user+channel,'context'] = json.dumps(context)

                #output to slack is done here
                output_command(channel, slack_output)
                conversation_id = context['conversation_id']

                try:
                    if context['currentIntent'] in ['anything_else']:
                        follow_ind = 1
                    else:
                        follow_ind = 0
                except:
                    pass

                if current_action == 'end_conversation':
                    session_df = session_df[session_df.user != message_user+channel]
                    context = {}
                    current_action = ''

                end_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                processing_time = str((datetime.datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')).total_seconds())

            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection  to slack failed")