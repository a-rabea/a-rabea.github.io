# Source folders (on the staging mirror) for each project, in display order.
U = "/mnt/user-data/uploads/02 Portfolio/Case Studies/"
SK = U + "Sheikh Khalifa Hospital/03_Behance/SKHF_Behance_v2/"
sk_slides = "01_cover 02_contents 03_glance 04_location 05_campus 06_mission 07_vision 08_values 09_objectives 10_open_facilities 11_capabilities 12_units 13_floorplan 14_open_coe 15_coe 16_rehab 17_burn 18_trauma 19_open_clinical 20_institutes 21_surgical 22_medical 23_paediatric 24_womens 25_support 26_open_commit 27_technology 28_community 29_milestones 30_closing".split()
S = lambda n: SK + "slides/" + n + ".jpg"
M = lambda n: SK + "mockups/" + n + ".jpg"
skhf = ([M("01_wall"), M("02_covers"), SK + "00_overview_grid.jpg"] + [S(x) for x in sk_slides[0:9]] + [M("03_meeting_room")] +
        [S(x) for x in sk_slides[9:18]] + [M("04_tablet")] + [S(x) for x in sk_slides[18:25]] + [M("05_laptop"), M("06_ipad")] +
        [S(x) for x in sk_slides[25:30]] + [M("07_prints"), M("08_system")])
import glob
def g(p): return sorted(glob.glob(U + p))
SOURCES = {
 "mazeed":   {"cover": U+"Mazeed/03_Behance/00_cover_1616x1264.jpg", "frames": [f for f in g("Mazeed/03_Behance/*.jpg") if "00_cover" not in f]},
 "ideas-that-scale": {"cover": U+"Social Media Main Project/03_Behance/00_cover_1616x1264.jpg", "frames": [f for f in g("Social Media Main Project/03_Behance/*.jpg") if "00_cover" not in f]},
 "aureya":   {"cover": U+"Aureya/03_Behance/Aureya_Behance/00_cover_1616x1264.jpg", "frames": g("Aureya/03_Behance/Aureya_Behance/modules/*.jpg"), "video": U+"Aureya/03_Behance/Aureya_Behance/motion/Aureya_stories_reel.mp4"},
 "pizza-rush": {"cover": U+"Pizza Rush/03_Behance/PizzaRush_Behance/02_Project-Thumbnail/Thumb_B_Rushu-Vinyl_1616.jpg", "frames": g("Pizza Rush/03_Behance/PizzaRush_Behance/01_Upload-to-Behance_in-this-order/*.jpg")},
 "aywa":     {"cover": U+"AYWA/03_Behance/AYWA_Behance_v2_1/AYWA_Behance_v2/AYWA_00_thumbnail_C_1616x1264.jpg", "frames": g("AYWA/03_Behance/AYWA_Behance_v2_1/AYWA_Behance_v2/01_Behance_Images/*.jpg")},
 "vult":     {"cover": U+"VULT/03_Behance/VULT_Behance/02_thumbnails/vult_thumb_A.jpg", "frames": g("VULT/03_Behance/VULT_Behance/01_case_study_frames/*.jpg"), "video": U+"VULT/02_Exports/VULT_brand_in_motion_v3.mp4"},
 "qinwan":   {"cover": U+"Qinwan قنوان/03_Behance/Qinwan_Behance_v2/02b_Thumbnail_1616x1264_HiRes/Human-B_Unboxing.jpg", "frames": g("Qinwan قنوان/03_Behance/Qinwan_Behance_v2/01_Upload-to-Behance_in-this-order/*.jpg")},
 "sheikh-khalifa-hospital": {"cover": SK+"thumb_A_wall_1616x1264.jpg", "frames": skhf},
 "roava":    {"cover": U+"Roava/02_Exports/thumb_B_lime.jpg", "frames": g("Roava/03_Behance/roava_behance/frames/*.jpg")},
}
