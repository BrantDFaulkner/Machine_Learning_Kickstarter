
class KsUrl:

    def __init__(self, project_id, project_name):
        self.project_id = project_id
        self.project_name = project_name

    def gen_url(self):
        project_id = self.project_id[4:]
        name = self.project_name#.decode("utf-8")
        name = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '').replace('---', '-').replace('"', '').replace("'", '')[:50]
        project_url = "https://www.kickstarter.com/projects/" + project_id + "/" + name
        return  project_url

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




project_list =  [
    ("kkst139451001", "It Might Become a Movie", "https://www.kickstarter.com/projects/139451001/it-might-become-a-movie"),
    ("kkst1765345673", "365 Postcards", "https://www.kickstarter.com/projects/1765345673/365-postcards"),
    ("kkst858578162", "Up North Cookbook", "https://www.kickstarter.com/projects/858578162/up-north-cookbook"),
    ("kkst1714875186", "Take a postcard trip with Anita as she watercolors her way through Bosnia & Croatia", "https://www.kickstarter.com/projects/1714875186/take-a-postcard-trip-with-anita-as-she-watercolors")
]

# ksurl.test_generate(url_list)
KsUrlTest(project_list).test()


# ksurl = KsUrl("kkst139451001", "It Might Become a Movie")
#
# print ksurl.gen_url()

# url = ksurl.generate("kkst139451001", "It Might Become a Movie")
# print url
