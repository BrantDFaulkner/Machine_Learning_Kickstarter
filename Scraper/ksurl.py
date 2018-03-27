
class KsUrl:

    def __init__(self, project_id, project_name):
        self.project_id = project_id
        self.project_name = project_name

    # def gen_url(self):
    #     project_id = self.project_id[4:]
    #     #name = self.project_name.decode("utf-8")
    #     url_name = self.project_name
    #     make_changes_flag = True
    #     while make_changes_flag:
    #         url_name_orig = url_name
    #         url_name = self.format_project_name(url_name)
    #         make_changes_flag = url_name_orig != url_name
    #
    #     url_name = url_name[:50]

    def gen_url(self):
        project_id = self.project_id[4:]
        url_name = self.project_name
        project_url = "https://www.kickstarter.com/projects/" + project_id + "/" + url_name
        return  project_url

    def format_project_name(self, project_name):
        url_name = project_name.lower()
        substitutions = {
            " ": "-",
            "(": "",
            ")": "",
            ".": "",
            "--": "-",
            '"': "",
            "'": ""
        }

        for key, value in substitutions.items():
            url_name = url_name.replace(key, value)

        return url_name

class KsUrlTest:

    def __init__(self, project_list):
        self.project_list = project_list

    def test(self):
        for project in self.project_list:
            project_id = project[0]
            project_name = project[1]
            project_url = project[2]
            ksurl = KsUrl(project_id, project_name)
            gen_url = ksurl.gen_url()
            if project_url != gen_url:
                for x in [project_id, project_name, project_url, gen_url]:
                    print x
            else:
                print "Pass"
