import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd


def collect(coin):

    try:
        service = Service(executable_path="./chromedriver-linux64/chromedriver")
        driver = webdriver.Chrome(service=service)

        driver.get("https://coinmarketcap.com/")

        driver.maximize_window()
        time.sleep(2)

        search = driver.find_element(
            "xpath", "//div[contains(@class, 'sc-e20acb0c-1 bzOMtl')]"
        )
        search.click()
        time.sleep(2)

        a = search.find_element(
            by="xpath", value="//input[@class = 'sc-d565189d-3 ctOzuc desktop-input']"
        )
        json = {}
        json["coin"] = coin
        data = {}
        a.send_keys(f"{coin}")

        time.sleep(2)
        a.send_keys(Keys.ENTER + Keys.ENTER)

        time.sleep(2)
        price = driver.find_element(
            by="xpath", value="//span[@class='sc-d1ede7e3-0 fsQm base-text']"
        )

        print(price.text)
        data["price"] = float(price.text[1:])

        change = driver.find_element(
            by="xpath", value="//p[@class='sc-71024e3e-0 sc-58c82cf9-1 bgxfSG iPawMI']"
        )

        r = change.value_of_css_property("color")

        market_cap = driver.find_element(
            by="xpath", value="//dd[@class='sc-d1ede7e3-0 hPHvUM base-text']"
        )

        m_cap = market_cap.text.split("\n")
        if r == "rgba(22, 199, 132, 1)":

            data["price_change"] = float(f"+{m_cap[0][:-1]}")
        else:

            data["price_change"] = float(f" -{m_cap[0]}")
        data["market_cap"] = int((m_cap[1][1:]).replace(",", ""))

        time.sleep(2)

        rank = driver.find_element(
            by="xpath", value="//span[@class='text slider-value rank-value']"
        )

        data["market_cap_rank"] = int(rank.text[1:])
        vol_rank = driver.find_elements(
            by="xpath", value="//span[@class='text slider-value rank-value']"
        )
        data["volume_rank"] = int(vol_rank[1].text[1:])
        print(data)

        stat = driver.find_elements(
            by="xpath", value="//dd[@class='sc-d1ede7e3-0 hPHvUM base-text']"
        )

        data["circulating_supply"] = int(
            stat[-4].text[:-4].replace(",", "").split(" ")[0]
        )
        print(data)
        data["total_supply"] = int(stat[-3].text[:-4].replace(",", "").split(" ")[0])

        data["volume_change"] = float(stat[-5].text[:-2])
        data["diluted_market_cap"] = int(stat[-1].text[1:].replace(",", ""))

        social_links = driver.find_elements(
            by="xpath", value="//a[@rel='nofollow noopener']"
        )

        time.sleep(1)
        contract = {}

        if len(social_links) == 4:
            contract["whitepaper"] = "None"
        else:
            contract["whitepaper"] = social_links[2].get_attribute("href")

        contract["contract"] = social_links[0].get_attribute("href")
        contract["official_link"] = social_links[1].get_attribute("href")
        contract["twitter"] = social_links[-2].get_attribute("href")
        contract["telegram"] = social_links[-1].get_attribute("href")

        driver.quit()
        json["output"] = data
        json["links"] = contract
        print(json)
        return json

    except Exception as e:
        print("error@ = ", e)

        driver.quit()


def run(list_coin):
    job = []

    for coin in list_coin:

        job.append(collect(coin))
    print(job)
    df = pd.DataFrame(
        [
            {
                "coin": item["coin"],
                "price": item["output"]["price"],
                "price_change": item["output"]["price_change"],
                "market_cap": item["output"]["market_cap"],
                "market_cap_rank": item["output"]["market_cap_rank"],
                "volume_rank": item["output"]["volume_rank"],
                "volume_change": item["output"]["volume_change"],
                "circulating_supply": item["output"]["circulating_supply"],
                "total_supply": item["output"]["total_supply"],
                "diluted_market_cap": item["output"]["diluted_market_cap"],
                "contract_link": item["links"]["contract"],
                "official_link": item["links"]["official_link"],
                "whitepaper_link": item["links"]["whitepaper"],
                "twitter_link": item["links"]["twitter"],
                "telegram_link": item["links"]["telegram"],
            }
            for item in job
        ]
    )
    print(df)
    df.to_excel("output.xlsx", index=False)
    # df.to_csv("output.csv")

    return job


# run(["NOT", "DUKO", "GORILLA"])
# ["NOT", "DUKO", "GORILLA"]
