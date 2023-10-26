# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# ohtani driver_path = "C:\\Users\\ip2305\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
driver_path = r'D:\AUC\bin\edgedriver_win64\msedgedriver.exe'
service = Service(executable_path=driver_path) # 2) executable_pathを指定
driver = webdriver.Edge(service=service) # 3) serviceを渡す
from selenium.webdriver.common.by import By


#################################################################################################################
#### Thanks: https://stackoverflow.com/questions/23223018/selenium-get-all-iframes-in-a-page-even-nested-ones
#################################################################################################################
def get_table_data(driver, table_id=-1):
    table_all = driver.find_elements(By.TAG_NAME, 'table')
    # table_idが -1の時は全部。正の時はその番号のテーブル
    tables = table_all if table_id == -1 else [table_all[table_id]]
    for table in tables:
        trs = table.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, 'td')
            td_data = [td.text for td in tds]
            print(td_data)
        pass
    pass
    return

def list_tags(driver, tag, attr, tab=''):
    tags = driver.find_elements(By.TAG_NAME, tag)
    print(f'{tab}{tag}_count={len(tags)}, {tag}s.{attr}[] =',  [sp.get_attribute(attr) for sp in tags if sp.get_attribute(attr) is not None])

def try_all_iframes(driver, tab=''):
    tag = 'span'
    attr = 'id'
    list_tags(driver, tag, attr, tab)
    stag = 'iframe'
    iframes = driver.find_elements(By.XPATH, f"//{stag}")
    if len(iframes) == 0:
        print(f'{tab} no iframes')
    #
    for index, iframe in enumerate(iframes):
        # Your sweet business logic applied to iframe goes here.
        print(f'{tab}iframe.id,name = {iframe.get_attribute("id")}, {iframe.get_attribute("name")}')
        driver.switch_to.frame(index)
        #
        list_tags(driver, tag, attr, tab)
        #
        try_all_iframes(driver, tab+'\t')
        driver.switch_to.parent_frame()


#################################################################################################################
driver.get("https://stock-marketdata.com/china-containerized-freight-index")

get_table_data(driver)                      # 複数あるtable全部 出力
#get_table_data(driver, table_id=1)         # table_idで指定した tableのみ出力
try_all_iframes(driver)
###frametree = iframe_search([], driver)


# ページ内のテーブルを取得
iframes = driver.find_elements(By.TAG_NAME,"iframe")
driver.switch_to.frame(iframes[0])
trs1=driver.page_source
driver.switch_to.default_content()
driver.switch_to.frame(iframes[1])
trs2=driver.page_source
driver.switch_to.default_content()
driver.switch_to.frame(iframes[2])
trs3=driver.page_source
pass
#rows = iframes.find_elements_by_tag_name('tr')
#for row in rows:
#    columns = row.find_elements_by_tag_name('td')
 #   for column in columns:
  #      print(column.text)
#<iframe name="__uspapiLocator" src="about:blank" style="display: none; width: 0px; height: 0px; border: none; z-index: -1000; left: -1000px; top: -1000px;"></iframe>