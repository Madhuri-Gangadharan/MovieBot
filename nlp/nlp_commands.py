import os,sys
sys.path.append(os.path.abspath('/Users/madhuri/Documents/MS/Fall-2020/IS/Movie-Recommendation-Chatbot'))
from config import service, workspace_id
from nlp.nlp_solutions.nlplearn import *
from slack_files.slack_commands import slack_tiles, message_buttons


def handle_command(message, channel, message_user,context):
    current_action = ''
    #here we send message to assistant
    response = service.message(
    workspace_id = workspace_id,
    input = {'text': message},
    context = context).get_result()
       
    try:
        slack_output = ''.join(response['output']['text'])
    except:
        slack_output = ''
    

    context = response['context']
    
    try:
        search_key = response['entities'][0]['value']
    except:
        search_key = ''
    
    try:
        search_term = str(response['context']['movie_name'])
    except:
        search_term = ''
        
    res = ''

    try:
        if response['context']['currentIntent'] == 'hello' and search_term.strip() != '' and str(response['context']['option']) in ['1','2','3','4','5']:
            
            selection = int(response['context']['option']) - 1
            b = similarity_search(search_term, list(metadata.index))
            response['context']['movie_name'] = metadata.loc[b]['title'].values[selection]
            search_term = ''
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'hello' and search_term.strip() != '':
            
            b = similarity_search(search_term, list(metadata.index))
            results, links = metadata.loc[b]['title'], metadata.loc[b]['imdbURL']
            message_buttons(channel, results, links, 'Showing results for "' + str(search_term) + '" movie search')
    except:
        pass

    try:
        if response['context']['currentIntent'] == 'recommend_movies':
            
            a = get_recommendations(search_term)
            title, title_url, image_url = a, metadata.loc[a.index]['imdbURL'], metadata.loc[a.index]['ImageURL']
            slack_tiles(channel, search_term, title, title_url, image_url)
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'votes':
            res = str(metadata[metadata['title'] == search_term]['vote_average'].values[0])
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'adult_content':
            if metadata[metadata['title'] == search_term]['adult'].values[0] == 'True':
                res = 'This is an adult movie. Please dont watch this movie with Kids.'
            else:
                res = 'This is not an adult movie. You can watch this movie with Kids.'
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'genre':
            res = str(metadata[metadata['title'] == search_term]['genres'].values[0])
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'revenue':
            res = '$' + "{:,}".format(int(metadata[metadata['title'] == search_term]['revenue'].values[0])) 
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'overview':
            res = str(metadata[metadata['title'] == search_term]['overview'].values[0]) 
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'imdb':
            res = str(metadata[metadata['title'] == search_term]['imdbURL'].values[0]) 
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'tmdb':
            res = str(metadata[metadata['title'] == search_term]['tmdbURL'].values[0]) 
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'budget':
            res = '$' + "{:,}".format(int(metadata[metadata['title'] == search_term]['budget'].values[0]))
    except:
        pass
    
    try:
        if response['context']['currentIntent'] == 'vote_count':
            res = "{:,}".format(int(metadata[metadata['title'] == search_term]['vote_count'].values[0]))
    except:
        pass
    
    slack_output = slack_output + str(res)
    
    if slack_output == '' and search_term.strip() == '':
        slack_output = '"' + str(search_term) + '" does not exists. Please check'        
    
    if 'actions' in response:
        if response['actions'][0]['type'] == 'client':
            current_action = response['actions'][0]['name']
   
    return(context,slack_output,current_action)