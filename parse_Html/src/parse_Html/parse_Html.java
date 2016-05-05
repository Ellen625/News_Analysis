package parseHtml;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import java.awt.List;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import javax.lang.model.element.Element;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements; 

public class parsehtml {

	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		BufferedReader br = new BufferedReader(new FileReader("./NYTimes_left3.csv"));
		String line;
		String csv = "./NYTimes_left3_content.csv";
		FileWriter writer = new FileWriter(csv);
		String articles; 
		String id;
		while((line = br.readLine())!=null){
			//System.out.println(line);
			String dataset[] = line.split(",");
			
			Document doc = (Document) Jsoup.connect(dataset[2])
					.cookie("NYT-S","0MrwnLER.2CRfDXrmvxADeHzlw4hz1ELt2deFz9JchiAIUFL2BEX5FWcV.Ynx4rkFI")
					.cookie("nyt-m","63FC54E06CAA9BFAA93534C40246E306&e=i.1422766800&t=i.10&v=i.1&l=l.15.829753007.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1&n=i.2&g=i.0&rc=i.0&er=i.1419483874&vr=l.4.1.1.0.0&pr=l.4.1.1.0.0&vp=i.1&gf=l.10.829753007.-1.-1.-1.-1.-1.-1.-1.-1.-1&ft=i.0&fv=i.0&gl=l.2.-1.-1&rl=l.1.-1&cav=i.1&imu=i.1&igu=i.1&prt=i.5&kid=i.1&ica=i.1&iue=i.0&ier=i.0&iub=i.0&ifv=i.0&igd=i.0&iga=i.1&imv=i.1&igf=i.0&iru=i.0&ird=i.0&ira=i.1&iir=i.1&gb=l.3.1.5.1416978000")
					.cookie("NYT-wpAB", "0002|1&0012|1&0014|-2")
					.referrer("http://www.nytimes.com/")
					.timeout(0)
					.get();
            System.out.println(dataset[2]);
			org.jsoup.nodes.Element content = doc.getElementById("content");
			Elements p = doc.getElementsByTag("p");
			
			
			
			for (org.jsoup.nodes.Element i:p){
				String tag = i.tagName();
				if(tag.equals("p")){
					
					//test = test +i.text();
					articles = i.text().replaceAll("[,]","");
					//articles = i.text();
					writer.append(articles);
					
					System.out.println(articles);
					//writer.append(test);
					//System.out.println(i.text());
				}
				
			}
			writer.append(",");
			writer.append(dataset[0]);
			System.out.println(dataset[0]);
			
			writer.append("\n");
			
		}
		
		writer.flush();
		writer.close();

	}

}
