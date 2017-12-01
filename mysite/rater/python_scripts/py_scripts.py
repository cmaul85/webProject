class view_flags:
    def __init__(self, g_flag="", l_flag="", o_flag="", auth_flag=""):
        self.git_hub_flag = g_flag
        self.linkedin_flag = l_flag
        self.owners_profile_flag = o_flag
        self.is_authenticated = auth_flag


def Get_flags(user_profile=None, o_flag="", auth_flag=""):
    if user_profile is not None:
        if user_profile.git_hub_username not in [None, ""]:
            git_hub_flag = True
        else:
            git_hub_flag = False
        if user_profile.linkedin_username not in [None, ""]:
            linkedin_flag = True
        else:
            linkedin_flag = False
        return view_flags(g_flag=git_hub_flag, l_flag=linkedin_flag, o_flag=o_flag)
    else:
        return view_flags(auth_flag=auth_flag)

class comment_object:
    def __init__(self, url, comment):
        self.rating_url = url
        self.comment = comment


def comment_list_converter(comment_list):
    new_comment_list = []
    pre_string = "/static/media/stars/"
    for i in comment_list:
        temp_comment = comment_object("star_{}.png".format(i.rating), i) 
        temp_comment.rating_url = pre_string + temp_comment.rating_url
        new_comment_list.append(temp_comment)
    return new_comment_list


# Use this function to get a rating out of the projects
def convert_project_rating(project):
    pre_string = "/static/media/stars/"
    if project.number_of_ratings == 0:
        return pre_string + "star_0.png"
    else:
        project_rating = project.rating / project.number_of_ratings
        if project_rating >= 1 and project_rating < 1.2:
            return pre_string + "star_1.png"
        elif project_rating >= 1.2 and project_rating < 1.8:
            return pre_string + "star_15.png"
        elif project_rating >= 1.8 and project_rating < 2.2:
            return pre_string + "star_2.png"
        elif project_rating >= 2.2 and project_rating < 2.8:
            return pre_string + "star_25.png"
        elif project_rating >= 2.8 and project_rating < 3.2:
            return pre_string + "star_3.png"
        elif project_rating >= 3.2 and project_rating < 3.8:
            return pre_string + "star_35.png"
        elif project_rating >= 3.8 and project_rating < 4.2:
            return pre_string + "star_4.png"
        elif project_rating >= 4.2 and project_rating < 4.8:
            return pre_string + "star_45.png"
        elif project_rating >= 4.8 and project_rating <= 5:
            return pre_string + "star_5.png"


class project_object:
    def __init__(self, project):
        self.project = project
        self.rating = convert_project_rating(project)


def search_project_name(search_query, project_name):
    if search_query in project_name:
        return True
    else:
        return False

def search_project_tags(search_query, tags):
    if search_query in tags:
        return True
    else:
        return False

def search_project_desc(search_query, description):
    if search_query in description:
        return True
    else:   
        return False

def search_project_user(search_query, username):
    if search_query == username:
        return True
    else:
        return False


def get_porject_list(projects, search_query, advanced_search=None):
    project_object_list = []
    if search_query == None or search_query == "":
        for i in projects:
            project_object_list.append(project_object(i))
        return project_object_list
    else:
        if advanced_search == None:
            search_queries = [search_query, ]
            #search_queries = search_quers.split('')  ## SOME DELIMITER
            for i in search_queries:
                for j in projects:
                    if (search_project_name(i, j.name) or
                        search_project_tags(i, j.tags.split(',')) or
                        search_project_desc(i, j.description) or
                        search_project_user(i, j.user.username)):
                        project_object_list.append(project_object(j))
                        
                    """
                    search_list = [j.name, j.description, j.user.username, j.tags.split(',')]
                    for k in search_list:
                        if i in k:
                            project_object_list.append(project_object(j))
                            break
                    """
            return project_object_list
        else:       ## User does advanced search
            print("error")




# check project title
# check description
# check username
# check tags


























