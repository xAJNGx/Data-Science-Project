import scrapy
import pandas as pd


class Province5Spider(scrapy.Spider):
    name = "province5"
    allowed_domains = ["annapurnapost.com"]
    start_urls = ["https://annapurnapost.com/category/provience5/"]
    
    scraped_data=[]

    def parse(self, response):
        
        articlesblock= response.xpath('//div[@class="card__details"]')
        
        for article in articlesblock:
            Category = article.xpath(".//div[@class='card__category']/a/text()").get()
            Title = article.xpath(".//h3[@class='card__title']/a/text()").get()
            Link = article.xpath(".//h3[@class='card__title']/a/@href").get()
            absoluteurl=f"https://annapurnapost.com/{Link}"
            # Do something with Category, Title, and Link (e.g., yield or process the data)
            yield scrapy.Request(absoluteurl, callback=self.parse_article_content, meta={'Category': Category, 'Title': Title,'Link':absoluteurl})
        
            
        next_page = response.xpath('//div[@class="pagination__right"]/a[@class="arrow next"]/@href').get()
    
        if next_page is not None:
           next_page_url =  next_page
           yield response.follow(next_page_url, callback=self.parse)
  
    def parse_article_content(self, response):
        Category = response.meta.get('Category')
        Title = response.meta.get('Title')
        Link = response.meta.get('Link')
        Author = response.xpath('//div[@class="post__meta"]/div[@class="author"]/p[@class="author__name"]/a/text()').get()
        Date = response.xpath('//div[@class="post__meta"]/p[@class="date"]/span/text()').get()
        Location =response.xpath('//div[@class="news__details"]/p/strong/text()').get()
        Content = response.xpath('//div[@class="news__details"]//text()').getall()
        
        #removing \n and spaces
        Content = [text.strip() for text in Content if text.strip()]
        Content = " ".join(Content)
        
        unwanted_text = ['\n                \n\n                ','\xa0:\xa0',"['\n                \n                ', '\n                    ', '\n                    ', '\n                    ', '\n                    ', '\n                       ",'\n','\xa0']  
        for text in unwanted_text:
            Content = Content.replace(text, '')
        self.scraped_data.append( {
            "Category": Category,
            "Title": Title,
            "Author": Author,
            "Date" : Date,
            "Location" : Location,
            "Content": Content,
            "Link": Link,
        })           
      
    def closed(self, reason):
        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(self.scraped_data)

        # Save the DataFrame to an Excel file
        df.to_excel("Province5.xlsx", index=True)        
