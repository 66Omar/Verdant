import time


def get_download_link(worker, driver, url, load_time, quality):
    link = url
    driver.get(link)
    driver.find_element_by_class_name('nobr').click()
    time.sleep(load_time)
    worker.state.emit(30)
    search = driver.find_elements_by_tag_name('tbody')
    search = search[1]
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    available_qualities = []
    for row in search.find_elements_by_tag_name('tr'):
        for cell in row.find_elements_by_tag_name('td'):
            if 'MB' not in cell.text and has_number(cell.text):
                available_qualities.append(strip_string(cell.text))
    worker.state.emit(40)
    quality = closest(quality, available_qualities)
    for row in search.find_elements_by_tag_name('tr'):
        for cell in row.find_elements_by_tag_name('td'):
            if str(quality) in str(cell.text):
                down_btn = row.find_element_by_class_name('tar')
                down_btn.find_element_by_tag_name('a').click()

    driver.switch_to.window(driver.window_handles[1])
    download_page = driver.current_url

    driver.get(download_page)
    driver.find_element_by_tag_name('h2').click()
    name = driver.find_element_by_tag_name('h2').text
    worker.state.emit(50)
    time.sleep(load_time)
    driver.refresh()
    download_page = driver.find_elements_by_tag_name('a')
    download_link = download_page[5].get_attribute('href')

    worker.state.emit(60)

    return [download_link, name]


def has_number(text):
    for each in text:
        if each in '1234567890':
            return True
    return False


def strip_string(text):
    new = ''
    for each in text:
        try:
            int(each)
            new += each
        except ValueError:
            pass
    return new


def closest(text, available):
    diff = 0
    quality = 0
    first = True
    for each in available:
        if first:
            diff = int(text) - int(each)
            quality = each
            first = False
        if abs(int(text) - int(each)) < abs(diff):
            diff = int(text) - int(each)
            quality = each
        if abs(int(text)) - int(each) == abs(diff):
            quality = max(int(quality), int(each))
    return str(quality)
