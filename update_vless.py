# update_vless.py — автообновление Vless ключей с проверкой через Xray (как в Happ)
import json
import subprocess
import random
import os

# Твои запасные ключи (вставь сюда свои реальные)
BACKUP_KEYS = [
    "vless://f6036ea2-911e-4287-93fb-d3ac2b21135b@node1.telegavpn.org:443?security=reality&type=tcp&headerType=&path=&host=&flow=xtls-rprx-vision&sni=node1.telegavpn.org&fp=&pbk=WvNaAxI0W__qfUKbtysH4IwF155YENlv3PG6crCmPkA&sid=#%F0%9F%87%A6%F0%9F%87%B9%20Austria%2C%20Vienna%20%5BBL%5D",
"vless://ab321a49-bc9c-4bb6-915b-a1fcbc7de49c@27.50.48.155:443?mode=gun&security=tls&encryption=none&alpn=h2,http/1.1&authority=&fp=chrome&type=grpc&serviceName=&sni=vbox1.ping-box.com#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@81.85.72.197:443?type=ws&security=tls&path=/&sni=sni.111000.indevs.in#%F0%9F%87%AB%F0%9F%87%AE%20Finland%2C%20Vantaa%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@185.228.233.22:443?encryption=none&security=tls&sni=sni.111000.v6.navy&insecure=0&allowInsecure=0&type=ws&host=sni.111000.v6.navy&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%2B%40WangCai2#%F0%9F%87%AC%F0%9F%87%AA%20Georgia%2C%20Tbilisi%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@185.128.106.42:443?encryption=none&security=tls&sni=sni.111000.indevs.in&fp=chrome&type=ws&host=sni.111000.indevs.in&path=/?ed%3D2560&packetEncoding=xudp#%F0%9F%87%AC%F0%9F%87%AA%20Georgia%2C%20Tbilisi%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@185.82.127.156:443?encryption=none&security=tls&sni=sni.111000.indevs.in&insecure=0&allowInsecure=0&type=ws&host=sni.111000.indevs.in&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%40%40jdfxq#%F0%9F%87%AC%F0%9F%87%AA%20Georgia%2C%20Tbilisi%20%5BBL%5D",
"vless://aaaaaabb-4ddd-4eee-9fff-ffffffffffff@afrcloud22.mmv.kr:443?encryption=none&security=tls&type=ws&host=afrcloud22.mmv.kr&path=%2F47.81.9.160%3D443&sni=afrcloud22.mmv.kr#%F0%9F%87%B9%F0%9F%87%AD%20Thailand%2C%20Bangkok%20%5BBL%5D",
"vless://aaaaaabb-4ddd-4eee-9fff-ffffffffffff@afrcloud22.mmv.kr:443?encryption=none&security=tls&type=ws&host=afrcloud22.mmv.kr&path=%2F199.21.175.187%3D8443&sni=afrcloud22.mmv.kr#%F0%9F%87%B9%F0%9F%87%AD%20Thailand%2C%20Soeng%20Sang%20%5BBL%5D",
"vless://442ed0ac-c945-41ee-8bb5-8ee69ef50456@daltoon.best-cloud.ir:8443?encryption=none&type=xhttp&mode=auto&host=speed.daltoon-server.ir&path=%2F%3Fed%3D2056&security=tls&alpn=h2%2Chttp%2F1.1&fp=chrome&sni=speed.daltoon-server.ir#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Nuremberg%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@46.32.184.211:443?encryption=none&security=tls&sni=sni.111000.indevs.in&insecure=0&allowInsecure=0&type=ws&host=sni.111000.indevs.in&path=%2F%3FTelegram%F0%9F%87%A8%F0%9F%87%B3%40%40jdfxq%3D#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%2C%20Riga%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@212.193.4.209:443?type=ws&security=tls&encryption=none&sni=sni.111000.indevs.in&path=/%3FTelegram%25F0%259F%2587%25A8%25F0%259F%2587%25B3%2540WangCai2%3D&host=sni.111000.indevs.in&ed=2560&eh=Sec-WebSocket-Protocol#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Dreieich%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@66.151.40.21:8443?encryption=none&security=tls&sni=sni.111000.indevs.in&type=ws&host=sni.111000.indevs.in&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%40WangCai2#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Dreieich%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@77.221.138.138:443?path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai2&security=tls&encryption=none&insecure=0&host=sni.111000.v6.navy&type=ws&allowInsecure=0&sni=sni.111000.v6.navy#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Dreieich%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@92.42.96.223:443?encryption=none&security=tls&sni=sni.111000.indevs.in&type=ws&host=sni.111000.indevs.in&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%40WangCai2#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Dreieich%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@92.42.96.223:443?security=tls&type=ws&path=%2F%3Fed%3D2560&host=sni.111000.indevs.in&sni=sni.111000.indevs.in#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Dreieich%20%5BBL%5D",
"vless://eb071647-72a6-46be-8e89-ff3d228d52f6@at.jojack.ru:443/?type=tcp&encryption=none&flow=xtls-rprx-vision&sni=at.jojack.ru&fp=chrome&security=reality&pbk=ca5sfJNcjkh3oNt51hRexXbGWgITAqCprGSU-YKCJBA&sid=8dc4fccb2bcfc99d#%F0%9F%87%A6%F0%9F%87%B9%20Austria%2C%20Vienna%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@92.53.191.238:2096?path=/?ed=2560&/Join-V2rayTun0-Join-V2rayTun0-Join-V2rayTun0-Join-V2rayTun0-Join-V2rayTun0-Join-V2rayTun0-Join-V2rayTun0-Join-V2rayTun0-&security=tls&encryption=none&insecure=0&host=sni.jpmj.dev&type=ws&allowInsecure=0&sni=sni.jpmj.dev#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@188.227.86.12:30718?encryption=none&security=tls&sni=sni.111000.v6.navy&insecure=0&allowInsecure=0&type=ws&host=sni.111000.v6.navy&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai2#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Istres%20%5BBL%5D",
"vless://5757c746-9878-4cfd-874a-edd95485f26d@fr.fasti.win:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=CuLjZaOWwaC_didE-f8CZoUK0mGH75iq-0u1St_wjUU&sid=67f8515f3fa23d2f&sni=fr.fasti.win#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Paris%20%5BBL%5D",
"vless://18f72be7-0651-4037-928b-8a309d685796@fr.pineappled.org:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=qFBIVGsvXTMeJcdJz6GiL7DG0XNhCg7rItza7t0qTgU&sid=9eb31eb7572c0882&sni=google.com#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Paris%20%5BBL%5D",
"vless://f6d382fa-3a53-4497-beb0-b285ac9bcf3a@fr.fasti.win:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=CuLjZaOWwaC_didE-f8CZoUK0mGH75iq-0u1St_wjUU&sid=67f8515f3fa23d2f&sni=fr.fasti.win#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Paris%20%5BBL%5D",
"vless://f7ddcea8-95e3-48de-909f-bb5d3c47696b@45.132.185.227:889#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Paris%20%5BBL%5D",
"vless://ccedb1b1-35f3-46d1-a85a-c699eef5f3e1@fran.scroogethebest.com:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=random&pbk=AYQOZFxjvHN-RIzKYEibwFiFsp03cdlWGdCmyFfuNVc&sid=4fa44664f6a566d3&sni=fran.scroogethebest.com&spx=/#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Paris%20%5BBL%5D",
"vless://07cd9dbe-21ac-4871-817d-c772687e4b7c@37.16.74.19:2053?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=WckOSneVajAzpH0sZSAFAWPnmwuuEXKZrTICNj5_hHU&sid=4a5b6c7d&sni=www.ibm.com#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Zuidoost%29%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://c73b5c37-0c2b-4d78-8a48-d32bba7432b4@188.212.125.121:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=chrome&pbk=kEwGhfvGuVsFGuK_udvrytSKGb081PL3Z_hBDAgDzS0&sid=9c2378562188c3cb&sni=nl.kickvpn.ru&path=&host=&spx=/#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Dronten%20%5BBL%5D",
"vless://f4d11a91-c69e-3a9e-8224-3379e00ae9c4@au04.fjk.wtf:1600?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.apple.com&fp=chrome&pbk=Vc8ycAgKqfRvtXjvGP0ry_U91o5wgrQlqOhHq72HYRs&sid=1bc2c1ef1c&type=tcp&headerType=none#%F0%9F%87%A6%F0%9F%87%BA%20Australia%2C%20Alexandria%20%5BBL%5D",
"vless://eb071647-72a6-46be-8e89-ff3d228d52f6@by.cdn.titun.su:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=0L6FE1vTechnKhN9LxFgmcDzqGVIfEQz8ZBGfvzKGzg&sid=cad317b20db4aad2&sni=by.cdn.titun.su#%F0%9F%87%A7%F0%9F%87%BE%20Belarus%2C%20Minsk%20%5BBL%5D",
"vless://e4fc4761-154f-490e-bbaa-b4fa193f1073@45.148.31.0:15855?path=%2F&security=&encryption=none&host=45.148.31.0&fp=chrome&type=ws#%F0%9F%87%A9%F0%9F%87%B0%20Denmark%2C%20Asperup%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@77.105.163.138:2096?security=tls&type=ws&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%40WangCai2&host=sni.111000.indevs.in&sni=sni.111000.indevs.in&fp=chrome&encryption=none#%F0%9F%87%A8%F0%9F%87%A6%20Canada%2C%20Toronto%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@185.18.250.238:2096/?security=tls&type=ws&path=/?ed=2560&host=sni.jpmj.dev&sni=sni.jpmj.dev&fp=chrome&encryption=none#%F0%9F%87%A8%F0%9F%87%A6%20Canada%2C%20Toronto%20%5BBL%5D",
"vless://ff6fb512-147d-419a-9672-e131133f7189@93.115.25.194:8443?encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=L3X1eh1Jq_6PKJ6LlwjgiWq0XNaDOqCVKgIElJ5nkVA&security=reality&sid=e0ef3d5c0aacb615&sni=tradingview.com&type=tcp#%F0%9F%87%B1%F0%9F%87%B9%20Lithuania%2C%20%C5%A0iauliai%20%5BBL%5D",
"vless://7177f5c4-f26a-4ab5-820f-62cb6ba649f7@31.170.22.193:47997?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=qq&pbk=cFora2YYa3aZdpWW8vMD9iX97qRKtyLzXv4pWgXoh20&sid=ead461&sni=apple.com&spx=/#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%2C%20Riga%20%28Latgales%20priek%C5%A1pils%C4%93ta%29%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@185.242.106.215:443?encryption=none&security=tls&sni=sni.111000.indevs.in&insecure=0&allowInsecure=0&type=ws&path=%2F#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%2C%20Riga%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://3be95058-e4e5-40e2-b51c-db1e6313cb7c@s3.plan-vpn.ru:443?encryption=none&flow=xtls-rprx-vision&type=tcp&security=reality&fp=chrome&sni=s3.plan-vpn.ru&pbk=jWqot3VkePiX8XYqgBNokg55WJJ5nTis3XzX6p2uaWQ&sid=7e348aa57a53b203#%F0%9F%87%AA%F0%9F%87%B8%20Spain%2C%20Madrid%20%28San%20Blas%29%20%5BBL%5D",
"vless://c73b5c37-0c2b-4d78-8a48-d32bba7432b4@185.170.212.208:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=AquVU8LAYQ3ic9yjqg89WLoaqKydqCO2tiDo78CTNlg&sid=9c2378562188c3cb&sni=es.kickvpn.ru#%F0%9F%87%AA%F0%9F%87%B8%20Spain%2C%20Valencia%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@62.192.174.175:2053?path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai2&security=tls&encryption=none&insecure=1&host=sni.111000.indevs.in&type=ws&allowInsecure=1&sni=sni.111000.indevs.in#%F0%9F%87%B8%F0%9F%87%AA%20Sweden%2C%20Steninge%20%5BBL%5D",
"vless://aaaaaabb-4ddd-4eee-9fff-ffffffffffff@afrcloud22.mmv.kr:443?encryption=none&security=tls&type=ws&host=afrcloud22.mmv.kr&path=%2F193.122.126.64%3D53777&sni=afrcloud22.mmv.kr#%F0%9F%87%B0%F0%9F%87%B7%20South%20Korea%2C%20Yangcheondong%20%5BBL%5D",
"vless://aaaaaabb-4ddd-4eee-9fff-ffffffffffff@afrcloud22.mmv.kr:443?encryption=none&security=tls&type=ws&host=afrcloud22.mmv.kr&path=%2F175.202.135.114%3D12427&sni=afrcloud22.mmv.kr#%F0%9F%87%B0%F0%9F%87%B7%20South%20Korea%2C%20Chungju-si%20%28Judeok-eup%29%20%5BBL%5D",
"vless://990e5a63-71e4-4dca-b110-ea8f9bf9f54b@93.114.98.171:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=9hLM71lkMgoCAzQJ2WBv5TXI_4Lucl5DctQveS85A0Q&sid=1c&sni=www.amd.com#%F0%9F%87%B9%F0%9F%87%B7%20Turkey%2C%20Bah%C3%A7elievler%20%5BBL%5D",
"vless://5d91fed7-24fc-4ddf-80f1-589a1275035c@tbankru.outlinekeys.net:8443?encryption=none&security=reality&sni=01.img.avito.st&pbk=JmO_njtIe9q7HRanm_dx4BtPAGCkycJuDskOISPx_Sg&spx=%2F&type=xhttp&path=%2Fapi%2Fv2%2Fupdates&mode=auto&extra=%7B%22mode%22%3A%22stream-up%22%2C%22xmux%22%3A%7B%22cMaxReuseTimes%22%3A%2264-128%22%2C%22maxConcurrency%22%3A%228-16%22%2C%22maxConnections%22%3A0%2C%22hKeepAlivePeriod%22%3A0%2C%22hMaxRequestTimes%22%3A%22400-600%22%2C%22hMaxReusableSecs%22%3A%221800-3600%22%7D%2C%22noSSEHeader%22%3Afalse%2C%22noGRPCHeader%22%3Afalse%2C%22xPaddingBytes%22%3A%22100-1000%22%2C%22scMaxBufferedPosts%22%3A30%2C%22scMaxEachPostBytes%22%3A%22500000-1000000%22%2C%22scMinPostsIntervalMs%22%3A%2210-50%22%2C%22scStreamUpServerSecs%22%3A%2230-90%22%7D#%F0%9F%87%AA%F0%9F%87%AA%20Estonia%20%5B%2ACIDR%5D",
"vless://1295e422-068a-11f1-b042-1bd023c5f030@ua2.vpnjantit.com:10002?encryption=none&security=tls&insecure=0&allowInsecure=0&type=ws&path=%2Fvpnjantit#%F0%9F%87%BA%F0%9F%87%A6%20Ukraine%2C%20Kyiv%20%5BBL%5D",
"vless://5757c746-9878-4cfd-874a-edd95485f26d@gb.fasti.win:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=-YTGWg5DjsLDyaDfr1D83kiUK22LVcrK3yC53lqqigs&sid=feedbacc&sni=uk.fasti.win#%F0%9F%87%AC%F0%9F%87%A7%20United%20Kingdom%2C%20Blackburn%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@156.243.246.238:2096?encryption=none&security=tls&sni=sni.jpmj.dev&type=ws&host=sni.jpmj.dev&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%40WangCai2#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%2C%20Chicago%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@45.43.79.121:443?path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai2&security=tls&encryption=none&insecure=1&host=sni.111000.indevs.in&type=ws&allowInsecure=1&sni=sni.111000.indevs.in#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%2C%20Chicago%20%5BBL%5D",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@85.31.236.117:8443?path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai2&security=tls&encryption=none&insecure=0&host=sni.111000.v6.navy&type=ws&allowInsecure=0&sni=sni.111000.v6.navy#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Aulnay-sous-Bois%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BBL%5D",
"vless://cc976b15-418b-4f0b-89ce-cd685ffbaf20@vnn.vpnfreedom.tech:443?type=tcp&security=reality&pbk=odbiaA-5s0mkehtfrf2SBcrKAMDP1sFjxKHJYdDCKgc&fp=chrome&sni=google.com&sid=81&spx=/&flow=xtls-rprx-vision#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%5B%2ACIDR%5D%20VK",
"vless://3c5c4ccc-b502-42cb-8c42-cfa714db4767@37.139.33.15:443?encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=7zd9mJilgjOrg_ohtw23Vmio-pdnYqeP_r-kiWt87Cg&security=reality&sid=2715592069f36fe7&sni=m.vk.ru&type=tcp#%F0%9F%87%AD%F0%9F%87%BA%20Hungary%20%5B%2ACIDR%5D%20VK",
"vless://6202b230-417c-4d8e-b624-0f71afa9c75d@45.129.8.68:45631?encryption=none&security=tls&sni=sni.111000.indevs.in&insecure=0&allowInsecure=0&type=ws&host=sni.111000.indevs.in&path=%2F%3Fed%3D2560%26Telegram%F0%9F%87%A8%F0%9F%87%B3%2B%40WangCai2#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%5B%2ACIDR%5D",
"vless://eb905045-5eeb-45ac-b9de-424f18047ecc@ss.sps1.sbs:8443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&sni=dropbox.com#%F0%9F%87%AB%F0%9F%87%B7%20France%2C%20Gravelines%20%5BBL%5D",
"vless://eb4234b2-8083-4038-af1d-ae752b4ad6d4@130.193.59.133:8443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=_CjW0Khlrr5z5oc9Oy6-w2ZEanz-zMBktVn5EOX9oTM&sid=6419bed7fd0a2cff&sni=yandex.ru#%F0%9F%87%AE%F0%9F%87%B9%20Italy%20%5B%2ACIDR%5D%20YA",
"vless://853fb55f-e53f-460a-b562-e2683f14be4a@84.201.158.253:9443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=qq&pbk=dAkHO3gjVWh11tmbzFjAZu3Haxzvn5WN03J_Y_SlyCg&sid=c6e5d902&sni=api-maps.yandex.ru&path=&host=#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%5B%2ACIDR%5D%20YA",
"vless://e8accc46-c511-42fb-919b-9283799a88a1@79.137.175.56:443?encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=Qddpg8luihgzgx4g4uMJklXzlrMCd8L1igJSWrRUvSc&security=reality&sid=8f222b3475800821&sni=m.vk.ru&type=tcp#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%5B%2ACIDR%5D%20VK",
"vless://7bc30425-1c2f-4823-b629-90f599a4cbfe@5.188.140.18:1488?type=tcp&security=reality&flow=xtls-rprx-vision&fp=qq&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&sid=&sni=ads.x5.ru&path=&host=#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%5B%2ACIDR%5D%20VK",
"vless://30c04389-bbcb-431f-9d47-a8ad24406bd4@45.134.218.222:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=eQXsYV276NoiN9SDwuloNrJkX-NU2tDtkMK6ntKQwlg&sid=d4727968a1fae56f&sni=stats.vk-portal.net#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20stats.vk-portal.net",
"vless://4cf310ea-c23e-49ef-a19a-65500db26cdf@72.56.105.101:11032?encryption=none&flow=xtls-rprx-vision&security=reality&sni=music.yandex.ru&fp=chrome&pbk=LrREjbPlHG92QJd3wlfS6ZfNtDvfK1R0G7uOa4Mj2Bg&sid=221afa311f348098&packetEncoding=xudp#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20music.yandex.ru",
"vless://0c857f2a-835d-45ad-a5c3-c1ee0abeccb3@pay.enginecraft.ru:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=&pbk=1wvMytki5FvF0gE1XhnfekIPPEI4MQR5BIXpdO8bNXE&sid=&sni=eh.vk.com&path=&host=#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%5BSNI-RU%5D%20eh.vk.com",
"vless://681a694f-7242-4410-b7a0-57106933637d@5.175.134.3:31739?type=grpc&security=reality&fp=&pbk=n5GKmln6W2vSudQiotMEAu5ycZu-iKVJXRlCgXdHtx0&sid=e9b573&sni=xapi.ozon.ru&mode=gun&serviceName=xapi.ozon.ru&authority=xapi.ozon.ru#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20xapi.ozon.ru",
"vless://681a694f-7242-4410-b7a0-57106933637d@5.175.134.3:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=chrome&pbk=zTH3m7h5RrVagZ5WnwEEoJIpFhHFW0bcKKf68h7eMno&sid=&sni=xapi.ozon.ru&path=&host=#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20xapi.ozon.ru",
"vless://681a694f-7242-4410-b7a0-57106933637d@138.124.79.173:81?type=xhttp&security=reality&fp=random&pbk=Rb6WZ6zv_UlQcRiy33kUft1JlTKZ2KGgJt-CvVC5pSI&sid=7b6fbcd52f&sni=xapi.ozon.ru&host=xapi.ozon.ru&mode=auto#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20xapi.ozon.ru",
"vless://681a694f-7242-4410-b7a0-57106933637d@5.175.134.3:81?type=xhttp&security=reality&fp=&pbk=Rb6WZ6zv_UlQcRiy33kUft1JlTKZ2KGgJt-CvVC5pSI&sid=cf&sni=xapi.ozon.ru&host=xapi.ozon.ru&mode=auto#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20xapi.ozon.ru",
"ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpvWklvQTY5UTh5aGNRVjhrYTNQYTNB@82.38.31.62:8080?#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Noord%29%20%5BBL%5D",
"ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprMWRCT21PQjRvcWk3VW1wMzdhMWJR@82.38.31.214:8080#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Noord%29%20%5BBL%5D",
"ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprMWRCT21PQjRvcWk3VW1wMzdhMWJR@82.38.31.217:8080#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Noord%29%20%5BBL%5D",
"vless://74c94a27-a187-4759-a1bf-2170ce196288@nl04-vlr01.tcp-reset-club.net:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=chrome&pbk=mLmBhbVFfNuo2eUgBh6r9-5Koz9mUCn3aSzlR6IejUg&sid=86e999a2cdc2&sni=hls-svod.itunes.apple.com&path=&host=&spx=/#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Zuidoost%29%20%5BBL%5D",
"vless://9fdd70da-b710-48b7-945a-642fe8937861@nl04-vlr01.tcp-reset-club.net:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=chrome&pbk=mLmBhbVFfNuo2eUgBh6r9-5Koz9mUCn3aSzlR6IejUg&sid=e499f276e7bd6420&sni=hls-svod.itunes.apple.com&path=&host=&spx=/#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Zuidoost%29%20%5BBL%5D",

]

def test_vless_key(key: str) -> bool:
    """
    Жёсткий тест ключа через Xray — 1 в 1 как Happ проверяет "активен/неактивен"
    """
    try:
        # Простой парсинг ключевых параметров (можно улучшить под все случаи)
        uuid = key.split('://')[1].split('@')[0]
        addr_part = key.split('@')[1].split('?')[0]
        host, port_str = addr_part.rsplit(':', 1)
        port = int(port_str.strip())

        # Базовый конфиг для теста (SOCKS inbound + VLESS outbound)
        config = {
            "log": {"loglevel": "none"},
            "inbounds": [
                {"port": 10808, "protocol": "socks", "listen": "127.0.0.1"}
            ],
            "outbounds": [
                {
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": host,
                                "port": port,
                                "users": [{"id": uuid}]
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "security": "none"  # будет перезаписано ниже
                    }
                }
            ]
        }

        # Добавляем параметры из ключа (security, flow, sni и т.д.)
        params = key.split('?')[1].split('#')[0] if '?' in key else ""
        param_dict = dict(p.split('=') for p in params.split('&') if '=' in p)

        if 'security' in param_dict:
            config["outbounds"][0]["streamSettings"]["security"] = param_dict['security']
        if 'sni' in param_dict:
            config["outbounds"][0]["streamSettings"]["tlsSettings"] = {"serverName": param_dict['sni']}
        if 'flow' in param_dict:
            config["outbounds"][0]["settings"]["flow"] = param_dict['flow']

        # Сохраняем временный конфиг
        with open("test_config.json", "w") as f:
            json.dump(config, f)

        # Запускаем тест Xray
        result = subprocess.run(
            ["./xray", "run", "-test", "-c", "test_config.json"],
            timeout=20,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"ЖИВОЙ (Xray тест прошёл): {key[:50]}...")
            return True
        else:
            print(f"МЁРТВЫЙ (Xray тест провал): {key[:50]}... → {result.stderr[:150]}")
            return False

    except Exception as e:
        print(f"МЁРТВЫЙ (ошибка теста): {key[:50]}... → {str(e)[:100]}")
        return False

def get_live_backup():
    random.shuffle(BACKUP_KEYS)
    for key in BACKUP_KEYS:
        if test_vless_key(key):
            print(f"Выбран живой запасной: {key[:50]}...")
            return key
    print("Все запасные ключи мёртвые!")
    return None

def update_keys():
    input_file = "vless.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()

        headers = all_lines[:2] if len(all_lines) >= 2 else []

        keys = [line.strip() for line in all_lines[2:] if line.strip().startswith("vless://")]

        if not keys:
            print("Нет ключей после заголовков")
            return

        new_keys = []
        replaced_count = 0

        for key in keys:
            if test_vless_key(key):
                new_keys.append(key)
            else:
                live_replacement = get_live_backup()
                if live_replacement:
                    new_keys.append(live_replacement)
                    replaced_count += 1
                    print(f"Заменён → {live_replacement[:50]}...")
                else:
                    new_keys.append(key)
                    print(f"Мёртвый оставлен (нет живых запасных): {key[:50]}...")

        with open(input_file, "w", encoding="utf-8") as f:
            f.writelines(headers)
            f.write("\n".join(new_keys) + "\n")

        print(f"\nОбновлено! Заменено: {replaced_count}/{len(keys)} ключей")
        print("Заголовки сохранены:")

    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    print("Запуск проверки и обновления...")
    update_keys()
