import re
from lxml import etree
import requests

url = 'https://www.zhihu.com/search?type=live&q=%E4%B8%AD%E5%9B%BD'
cookies = {
"_xsrf": "tjsUR8TjATsxQhu7ByIvatfmtdv0NRre",
" _zap": "9b518481-8d89-4021-a738-4cc005d4740a",
" d_c0": "ACDn1Hhrcg6PTrqQjn1VAo_yvdlZ2ZOiJ08=|1540976752",
" capsion_ticket": "2|1:0|10:1541052643|14:capsion_ticket|44:Y2YwYmFlMDY0NTQzNGFmZGEzNWNhNzUyNWExMzgwZDg=|f3212b2f42e8517ff0cf3f439fa7b9725fbe4e5838ebad7d9ad5cf970a6a033d",
" q_c1": "5d206884b5c14555a2e918f198ee3daf|1541146941000|1541146941000",
" r_cap_id": "NDhiYWI2OGQyODQwNDUwMmIzNTAxZjgxNjkyZjE1ZGQ=|1541146941|2c439cce89c12393e32a0c8a5ccc18806696c6a0",
" cap_id": "OTEzZTE5MWFmYzQ5NDlmOWE3NTgzZTg5YWFkYjc1ZGE=|1541146941|802b4924968a230af44cff821a5d2554c9c66a08",
" l_cap_id": "NDJiMTk0NjRlMmE1NDFkNThhZDQ5NjgyYzg4ZDhiODM=|1541146941|810d21ff0147f139fd1afad0282889b2362bcfb9",
" __utmc": "155987696",
" __utmz": "155987696.1541497541.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
" __utma": "155987696.928993130.1541497541.1541497541.1541734649.2",
" tgw_l7_route": "931b604f0432b1e60014973b6cd4c7bc",
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '70.0.3538.67 Safari/537.36',
    # 'referer': 'https://www.zhihu.com/search?type=live&q=%E4%B8%AD%E5%9B%BD',
    # 'x-ab-param': 'top_tag_isolation=0;pin_ef=orig;top_hqt=0;top_nmt=0;top_promo=1;top_tagore=1;top_feedre_itemcf=31;top_gr_topic_reweight=0;top_free_content=-1;top_video_score=1;top_30=0;top_quality=0;se_entity=on;top_ntr=1;top_recall_tb_follow=71;top_sjre=0;top_tffrt=0;top_tr=0;se_dl=0;top_retag=0;top_root_mg=1;se_cm=1;top_pfq=0;top_recall_tb_long=51;top_yhgc=0;top_billboard_count=1;top_videos_priority=-1;top_hweb=0;top_topic_feedre=21;top_vd_op=0;top_billvideo=0;se_consulting_switch=off;top_newfollowans=0;top_new_feed=1;top_uit=0;tp_sft=a;top_gr_model=0;se_gi=0;top_billupdate1=2;top_tagore_topic=0;top_local=1;top_manual_tag=1;top_distinction=0;top_feedre=1;top_mt=0;top_spec_promo=1;top_login_card=1;top_tmt=0;se_minor_onebox=d;ls_new_score=0;top_nszt=0;top_nucc=0;top_vd_gender=0;pin_efs=orig;se_ingress=on;top_retagg=0;top_root_ac=1;top_universalebook=1;top_alt=0;top_billread=1;top_video_fix_position=0;top_yc=0;se_billboard=3;se_consulting_price=n;top_gif=0;top_no_weighing=1;top_root=0;ls_play_continuous_order=2;top_fqa=0;top_gr_auto_model=0;se_filter=0;se_refactored_search_index=0;top_billpic=0;top_mlt_model=0;tp_discussion_feed_card_type=0;top_memberfree=1;top_vdio_rew=0;tp_ios_topic_write_pin_guide=1;top_newfollow=0;top_an=0;top_follow_reason=0;top_nid=0;top_ab_validate=0;se_major_onebox=major;se_new_market_search=off;top_cc_at=1;se_dt=1;top_vd_rt_int=0;se_wiki_box=1;top_bill=0;top_wonderful=1;se_merger=1;top_feedre_rtt=41;top_hca=0;top_recommend_topic_card=0;top_roundtable=1;top_raf=n;top_rank=0;top_recall_core_interest=81;top_v_album=1;top_card=-1;top_sj=2;top_adpar=0;top_f_r_nb=1;top_recall=1;top_feedre_cpt=101;top_multi_model=0;se_correct_ab=0;top_is_gr=0;top_feedtopiccard=0;top_lowup=1;top_nuc=0;top_recall_deep_user=1;top_recall_follow_user=91;top_recall_tb_short=61;top_root_few_topic=0;top_slot_ad_pos=1;top_tuner_refactor=-1;top_video_rew=0;top_followtop=0;top_user_gift=0;top_vds_alb_pos=0;tp_discussion_feed_type_android=0;se_auto_syn=0;se_product_rank_list=0;top_nad=1;tp_write_pin_guide=3;se_relevant_query=old;top_billab=0;top_ebook=0;top_new_user_gift=0;ls_new_video=0;se_daxuechuisou=new;se_tf=1;top_ac_merge=0;tp_favsku=a;se_rescore=0;top_recall_tb=1;se_gemini_service=content;top_ad_slot=1;top_dtmt=2;top_fqai=0;top_test_4_liguangyi=1;top_root_web=0;zr_ans_rec=gbrank',
    'x-api-version': '3.0.91',
}
text = requests.get(url=url, headers=headers).text
search_hash_id = re.compile(r'"searchHashId":"(.*?)"}}').findall(text)[0]
print(search_hash_id)
search_hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=live&q=%E4%B8%AD%E5%9B%BD&correction=1&offset=5&limit=10' \
                  '&show_all_topics=0&search_hash_id={}'.format(search_hash_id)
print(search_hash_url)
print('-----------------------------------------------------------')
text = requests.get(search_hash_url, headers=headers, cookies=cookies).text
print(text)

# par = re.compile(r'<div class="List-item"><div class="ContentItem"><div class="ContentItem-main"><div class'
#                  r'="ContentItem-image"><a href="(.*?)" target="_blank"><div class="LiveAvatar-wrapper" style'
#                  r'="width:60px;height:60px"><img class="Avatar Avatar--large LiveAvatar-img" width="60" height="60" '
#                  r'src="(.*?)" srcSet="(.*?) 2x"/></div></a></div><div class="ContentItem-head"><h2 class="ContentItem'
#                  r'-title"><div><a href="(.*?)" target="_blank"><span class="Highlight">(.*?)</span></a><span class='
#                  r'"SearchItem-type"></span></div></h2><div class="ContentItem-meta"><div class="SearchItem-meta">'
#                  r'<div class="RichText ztext SearchItem-description Highlight">(.*?)</div><div class="SearchItem-'
#                  r'liveStatus"><span class="Search-liveStatusLink">讲者：<span class="UserLink"><div class="Popover">'
#                  r'<div id="null-toggle" aria-haspopup="true" aria-expanded="false" aria-owns="null-content">'
#                  r'<a class="UserLink-link" data-za-detail-view-element_name="User" target="_blank" href="(.*?)">'
#                  r'<span class="Highlight">(.*?)</span></a></div></div></span></span><span class="Search-liveStatusLink'
#                  r'">评价：<div class="Rating">(.*?)</div></span><span class="Search-liveStatusLink">(.*?)<!-- --> 人参与</span>')
# info = par.findall(text)[0]
# for i in info:
#     print(info.index(i))
#     print(info)

# html = etree.HTML(text)
# all_ls = html.xpath('//div[@class="List"]/div[1]/div[@class="List-item"]')
# for i in all_ls:
#     name = i.xpath('./div[@class="ContentItem"]//span[@class="Search-liveStatusLink"][2]//svg/@class')
#     print('-------------------------------------------------------------------------------')
#     ls = []
#     for j in name:
#         print(j)
#         ls.append(str(j))
#     print('all_star == ', ls.count('Icon Icon--rating'))
#     print('half_star == ', ls.count('Icon Icon--ratingHalf'))

# cook = '_xsrf=tjsUR8TjATsxQhu7ByIvatfmtdv0NRre; _zap=9b518481-8d89-4021-a738-4cc005d4740a; d_c0="ACDn1Hhrcg6PTrqQjn1VAo_yvdlZ2ZOiJ08=|1540976752"; capsion_ticket="2|1:0|10:1541052643|14:capsion_ticket|44:Y2YwYmFlMDY0NTQzNGFmZGEzNWNhNzUyNWExMzgwZDg=|f3212b2f42e8517ff0cf3f439fa7b9725fbe4e5838ebad7d9ad5cf970a6a033d"; q_c1=5d206884b5c14555a2e918f198ee3daf|1541146941000|1541146941000; r_cap_id="NDhiYWI2OGQyODQwNDUwMmIzNTAxZjgxNjkyZjE1ZGQ=|1541146941|2c439cce89c12393e32a0c8a5ccc18806696c6a0"; cap_id="OTEzZTE5MWFmYzQ5NDlmOWE3NTgzZTg5YWFkYjc1ZGE=|1541146941|802b4924968a230af44cff821a5d2554c9c66a08"; l_cap_id="NDJiMTk0NjRlMmE1NDFkNThhZDQ5NjgyYzg4ZDhiODM=|1541146941|810d21ff0147f139fd1afad0282889b2362bcfb9"; __utmc=155987696; __utmz=155987696.1541497541.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=155987696.928993130.1541497541.1541497541.1541734649.2; tgw_l7_route=931b604f0432b1e60014973b6cd4c7bc' + ';'
# inner = re.compile(r'(.*?)=(.*?);').findall(cook)
# for i in inner:
#     (a, b) = i
#     print('\"%s\": \"%s\"' % (a, b))
