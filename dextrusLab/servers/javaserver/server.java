import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

class server {
    public static int port = 8005;
    public static String outputFileName = "output.txt";
    public static FileWriter output;
    public static void main(String[] args) {
        try {
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            server.createContext("/", new MyHandler());
        server.setExecutor(null); 
        server.start();
        System.out.println("Server started at port " + port);
        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
    }
    
    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            FileWriter output = new FileWriter("output.txt",true);
            
            String methodName = exchange.getRequestMethod();
            String protocol = exchange.getProtocol() ;
            URI uri = exchange.getRequestURI() ;

            //Request Headers
            Headers exchangeHeaders = exchange.getRequestHeaders();
            Map<String, List<String>> headers = new HashMap<>();
            for(String key: exchangeHeaders.keySet()) {
                headers.put(key, exchangeHeaders.get(key));
            }
                        
            //Request Body
            InputStreamReader isr = new InputStreamReader(exchange.getRequestBody(), "utf-8");
            BufferedReader br = new BufferedReader(isr);
            int b;
            StringBuilder body = new StringBuilder();
            while ((b = br.read()) != -1) {
                body.append((char) b);
            }
            br.close();
            isr.close();
            
            String response_content = "Body length : "+ body.toString().length()  +"\nBody : "+body.toString();
            String log_content =
               methodName + " " + uri + " " + protocol +
              "\n<-------\nRequest-headers :\n"+headers+"\n\n" +
              response_content +
              "\n------->\n";
            
            exchange.sendResponseHeaders(200, response_content.getBytes().length);

            //response
            OutputStream os = exchange.getResponseBody();
            os.write(response_content.getBytes());
            os.close();
            System.out.println(log_content);
            
            //log file
            output.write(log_content);
            output.close();
        }
    }

}
