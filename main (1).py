"""MAMA | An Explainable Rule-Based Kitchen Troubleshooting Expert System.

University Artificial Intelligence Group Project - complete source, all 3 tasks.

Task 1 - Knowledge Base and Working Memory:
    - 20 structured IF-THEN rules, R1-R20, with IDs, facts, conclusions,
      advice, and explicit action priority.
    - Fact initialization, addition, retrieval, removal, and session reset.
Task 2 - Forward Chaining and Explanation Facility:
    - Iterative rule matching, inference of new facts, rule trace,
      priority-based conflict resolution, and understandable premises.
Task 3 - Interactive CLI and Testing:
    - Problem-specific multiple-choice questions, validated inputs,
      reprompting, and three reproducible end-to-end scenarios.

No third-party Python packages are required. This is a knowledge-based system,
not machine learning and not an automatically verified food-safety diagnosis.

Usage:
    python main.py                 # Run Arabic interactive CLI
    python main.py --demo-tests    # Show 3 documented scenarios and CLI transcripts
    python main.py --self-test     # Exhaustively check all 160 response paths
"""
from typing import List, Set


class Rule:
    """قاعدة IF–THEN واحدة؛ النصيحة جزء من القاعدة، وليست دالة منفصلة.

    variants: تغييرات في صياغة *نفس* نصيحة القاعدة حسب الإجابات.
    """
    def __init__(self, rule_id, conditions, conclusion, description,
                 priority, advice, variants=None, verdict="FIX"):
        self.rule_id = rule_id
        self.conditions = set(conditions)
        self.conclusion = conclusion
        self.description = description
        self.priority = priority
        self.advice = advice
        self.variants = variants or []
        self.verdict = verdict

    def choose_advice(self, facts):
        """نختار النصيحة المكتوبة في القاعدة اعتمادًا على حقائق المستخدم."""
        for required_facts, advice, verdict in self.variants:
            if set(required_facts) <= facts:
                return advice, verdict or self.verdict
        return self.advice, self.verdict


class InteractiveExpertSystem:
    """Task 1: قاعدة المعرفة، ذاكرة العمل، والأسئلة."""
    def __init__(self):
        # 20 قاعدة مسماة R1-R20. لكل قاعدة إجراء/نصيحة يخرج من الاستدلال.
        # بعض القواعد تضبط نصيحتها حسب إجابة المستخدم دون إضافة قواعد جديدة.
        self.rules: List[Rule] = [
            Rule("R1", ["cake_sank"], "cake_sank_assessed",
                 "إذا هبط الكيك، نحدد أولًا هل وسطه نيّ أو مستوي.", 80,
                 "إذا الكيك مستوي لكنه هبط، قصّيه مكعبات وقدّميه بطبقات مع كريمة. "
                 "الخبز مرة ثانية ما بيرفعه.",
                 [(["center_raw"], "🚨 وسط الكيك نيّ؛ لا تقدمينه. إذا توّه طالع من الفرن "
                   "رجّعيه يكمل استواء، واختبري الوسط بعود نظيف قبل التقديم.", "DO_NOT_SERVE")]),
            Rule("R2", ["cake_dry"], "cake_dry_assessed",
                 "الكيك الناشف يحتاج ترطيب بسيط، وقد يكون جف من طول الخبز.", 80,
                 "قطّعي الكيك الناشف، ورطّبي كل قطعة بقليل من شراب خفيف أو حليب "
                 "يناسب الحلى. وقفي قبل ما يصير معجّن.",
                 [(["baked_too_long"], "رطّبي قطع الكيك بكمية بسيطة من شراب خفيف. "
                   "بالمرة الجاية قللي وقت الخبز وابدئي بفحص الاستواء بدري.", None),
                  (["outside_dark"], "رطّبي الكيك شوي بشراب خفيف. بالمرة الجاية "
                   "خففي حرارة الفرن قليلًا وتابعي الاستواء؛ الوجه تحمّر بسرعة.", None)]),
            Rule("R3", ["cake_raw_inside"], "cake_raw_assessed",
                 "وسط الكيك نيّ، فلازم يكمل استواء قبل التقديم.", 80,
                 "🚨 لا تقدمين الكيك وهو نيّ من الوسط. إذا توّه طالع من الفرن، "
                 "رجّعيه يكمل استواء وتحققي بعود نظيف.",
                 [(["outside_dark", "just_baked"], "🚨 الوسط نيّ والوجه غامق؛ "
                   "لا تقدمينه. رجّعيه يكمل على حرارة أخف قليلًا وتحققي من الوسط بعود نظيف.", "DO_NOT_SERVE")],
                 verdict="DO_NOT_SERVE"),
            Rule("R4", ["ganache", "separated"], "ganache_separation_assessed",
                 "الغاناش منفصل؛ نحاول نرجّع الخليط متجانس بالتدريج.", 80,
                 "أضيفي ملعقة صغيرة موية دافئة للغاناش مع الخفق، وكرري "
                 "بكميات بسيطة حتى يصير ناعم. لا تكثرين السائل مرة وحدة.",
                 [(["ganache_cold"], "دفّي الغاناش قليلًا على حمام مائي دافئ، "
                   "ثم أضيفي ملعقة صغيرة موية دافئة واخفقي حتى يتجانس. زيدي شوي عند الحاجة.", None)]),
            Rule("R5", ["ganache", "too_thick"], "ganache_thickness_assessed",
                 "الغاناش ثقيل؛ طريقة التعديل تختلف حسب استخدامه.", 80,
                 "حرّكي الغاناش لين يلين، وعدّلي قوامه تدريجيًا حسب الاستخدام.",
                 [(["for_drizzle", "ganache_cold"], "دفّي الغاناش البارد شوي، "
                   "ثم أضيفي كريمة دافئة ملعقة صغيرة كل مرة لين يصير قابل للصب.", None),
                  (["for_drizzle"], "أضيفي كريمة دافئة للغاناش ملعقة صغيرة كل مرة "
                   "مع التحريك لين ينسكب بسهولة.", None),
                  (["for_spread"], "إذا تبغينه حشوة أو تغطية، خليه يلين بحرارة الغرفة "
                   "وقلّبيه، ولا تكثرين كريمة عشان ما يصير خفيف.", None)]),
            Rule("R6", ["pastry_cream", "too_thin"], "pastry_cream_assessed",
                 "كريمة الحلويات ما ثخنت؛ السبب يختلف حسب مرحلة الطبخ.", 80,
                 "إذا الكريمة انطبخت وبردت لكنها ظلت سائلة، الأفضل تسوين دفعة جديدة "
                 "وتضبطين مقدار النشا بدل تحشين فيها الحلى.",
                 [(["insufficient_cooking"], "إذا الكريمة طازجة ومحفوظة صح، "
                   "رجّعيها على نار متوسطة مع التحريك المستمر لين تثخن وتبدأ تطلع فقاعات، "
                   "ثم برّديها بسرعة بالثلاجة.", None)]),
            Rule("R7", ["yeast_dough", "not_rising"], "proofing_problem_found",
                 "عجينة الخميرة ما ارتفعت؛ نراجع حرارة المكان وهل انخبزت.", 80,
                 "إذا العجينة بمكان دافئ ولسه ما ارتفعت، تأكدي من صلاحية "
                 "الخميرة واتبعي وقت التخمير بالوصفة؛ لا تخبزينها قبل ما ترتفع.",
                 [(["already_baked"], "إذا خبزتي العجينة قبل ما ترتفع ما راح تتخمر "
                   "بعد الخبز. إذا الخبز مستوي، قطّعيه شرائح وحمّصيه.", None),
                  (["environment_cold"], "غطّي عجينة الخميرة وخليها بمكان دافئ "
                   "باعتدال وأعطيها وقت زيادة. لا تحطينها بفرن حار.", None)]),
            Rule("R8", ["proofing_problem_found", "environment_cold", "still_proofing", "food_safe"],
                 "warm_proofing_recommended",
                 "بما أن العجينة ما انخبزت والمكان بارد، نقدر نكمّل التخمير.", 60,
                 "غطّي عجينة الخميرة وخليها بمكان دافئ باعتدال. "
                 "راقبي زيادة حجمها بدل الاعتماد على الوقت فقط؛ لا تحطينها بفرن حار."),
            Rule("R9", ["bread_hard"], "bread_texture_assessed",
                 "الخبز قاسي؛ نميّز بين خبز يبس بعد فترة وخبز طلع قاسي من الفرن.", 80,
                 "إذا الخبز طلع قاسي من الفرن، قدّميه مع شوربة أو حمّصيه للغموس. "
                 "بالمرة الجاية انتبهي لكمية الدقيق ووقت الخبز.",
                 [(["bread_stale"], "رشي الخبز اليابس رشة موية خفيفة وسخّنيه "
                   "بالفرن كم دقيقة وقدّميه دافئ، بدون تبليل زيادة.", None),
                  (["excess_flour"], "إذا زدتي دقيق كثير وطلع الخبز قاسي من الفرن، "
                   "قدّميه محمّصًا مع غموس، وبالمرة الجاية التزمي بكمية الدقيق.", None)]),
            Rule("R10", ["too_sweet"], "sweetness_assessed",
                 "طريقة تقليل الإحساس بالحلاوة تعتمد على نوع الحلى.", 80,
                 "قدّمي قطعة صغيرة مع زبادي سادة أو كريمة بدون سكر؛ "
                 "السكر داخل الكيك ما نقدر نسحبه بعد الخبز.",
                 [(["sweet_liquid"], "زيدي حليب أو موية بدون سكر تناسب المشروب أو "
                   "الصوص، شوي شوي مع التذوق حتى ما يصير خفيف زيادة.", None)]),
            Rule("R11", ["too_salty"], "salt_problem_found",
                 "لتخفيف الملح نحدد نوع الطبخة وهل عندنا مكونات بدون ملح.", 80,
                 "زيدي من نفس مكونات الطبخة بدون ملح مثل الخضار أو الصوص الأساسي، "
                 "على دفعات صغيرة مع التذوق.",
                 [(["no_extra_ingredients"], "إذا ما عندك مكونات تزيدينها بدون ملح، "
                   "قدّمي كمية أقل مع إضافة جانبية غير مملحة لو تناسب الطبق؛ "
                   "البطاطس ما تسحب الملح بشكل سحري.", None),
                  (["rice_pasta"], "اطبخي كمية ثانية من الرز أو المكرونة بدون ملح "
                   "واخلطيها بالأولى تدريجيًا لين يتوازن الطعم.", None),
                  (["liquid_dish"], "زيدي مرق بدون ملح أو موية مناسبة للطبخة "
                   "بكمية بسيطة كل مرة وذوقي بعد التحريك.", None)]),
            Rule("R12", ["salt_problem_found", "liquid_dish", "unsalted_liquid_compatible", "food_safe"],
                 "dilution_recommended",
                 "الشوربة أو الصوص المالح ممكن نخففه بسائل مناسب بدون ملح.", 60,
                 "زيدي ربع كوب مرق غير مملح أو موية مناسبة للطبخة كل مرة، "
                 "ثم حرّكي وذوقي قبل الإضافة اللي بعدها."),
            Rule("R13", ["too_bitter"], "bitterness_assessed",
                 "نحدد هل المرارة من احتراق أو من مكوّن مثل القهوة والكاكاو.", 80,
                 "إذا المرارة مو من احتراق واضح، راجعي المكونات اللي زاد مقدارها "
                 "قبل ما تضيفين سكر عشوائي.",
                 [(["burnt_food"], "لا تخلطين الجزء المحروق مع الباقي. انقلي "
                   "الجزء السليم لوعاء نظيف؛ وإذا طعم الحرق منتشر اتركي الطبخة.", None),
                  (["bitter_cocoa"], "إذا المرارة من كاكاو أو قهوة في الحلى، "
                   "أضيفي شوي حليب أو كريمة مناسبة وذوقي قبل أي تعديل ثاني.", None)]),
            Rule("R14", ["surface_burn"], "surface_burn_assessed",
                 "احتراق السطح يختلف عن عدم استواء الجزء الداخلي.", 80,
                 "إذا السطح فقط محروق والباقي مستوي، شيلي الطبقة المحروقة بسكين نظيف. "
                 "إذا طعم الحرق منتشر، لا تستخدمين الجزء المتأثر.",
                 [(["inside_raw"], "🚨 شيلي الجزء المحروق من السطح، لكن لا تقدمين "
                   "الأكل لأن داخله باقي نيّ؛ لازم يكمل استواء أول.", "DO_NOT_SERVE")]),
            Rule("R15", ["severe_charring"], "discard_recommended",
                 "الأكل متفحّم بشكل كبير؛ ما نحاول ننقذه.", 100,
                 "🚨 الأكل متفحّم بشكل كبير. لا تحاولين تغطين طعم الحرق؛ تخلصي منه.",
                 verdict="DISCARD"),
            Rule("R16", ["missing_egg"], "egg_replacement_assessed",
                 "بديل البيض يتحدد حسب الوصفة والمكوّن المتوفر.", 80,
                 "إذا ما عندك بديل للبيض، اختاري وصفة كيك مكتوبة أصلًا بدون بيض.",
                 [(["egg_essential"], "الكاسترد والميرنغ يعتمدون على البيض؛ "
                   "الأفضل تختارين وصفة بدون بيض بدل تبديل المقادير عشوائيًا.", None),
                  (["simple_cake", "egg_substitute_compatible"],
                   "لكيك بسيط يقبل البدائل، استخدمي ربع كوب زبادي سادة بدل بيضة وحدة؛ "
                   "ممكن يصير القوام أثقل شوي.", None),
                  (["simple_cake", "have_banana"],
                   "لكيك بسيط يقبل البدائل، جرّبي ربع كوب موز مهروس بدل بيضة وحدة؛ "
                   "بيعطي طعم موز وقوام أثقل شوي.", None)]),
            Rule("R17", ["missing_cream"], "cream_replacement_assessed",
                 "بديل الكريمة يختلف إذا كانت للوصفة أو للخفق.", 80,
                 "إذا ما عندك بديل يناسب استخدام الكريمة، اختاري وصفة ما تحتاجها.",
                 [(["needs_whipping"], "كريمة الخفق ما يعوضها الحليب مع الزبدة "
                   "ولا الزبادي في التزيين؛ اختاري تغطية ثانية أو وفّري كريمة خفق.", None),
                  (["cold_dessert", "have_yogurt"], "للطبقات الباردة اللي ما تحتاج "
                   "خفق، جرّبي زبادي سادة ثقيل بدل جزء من القشطة، لكن طعمه أحمض شوي.", None),
                  (["creamy_sauce", "cream_substitute_compatible"],
                   "لصوص الطبخ، استخدمي حليب كامل الدسم مع شوية زبدة على نار هادئة "
                   "بالتدريج؛ ما ينفع هذا البديل للكريمة المخفوقة.", None)]),
            Rule("R18", ["missing_baking_powder"], "baking_powder_replacement_assessed",
                 "بديل البيكنج باودر يحتاج مقادير محسوبة ووصفة مناسبة.", 80,
                 "إذا ما عندك بديل محسوب، وفّري بيكنج باودر أو اختاري وصفة "
                 "مكتوبة أصلًا من دونه.",
                 [(["quick_bread", "baking_soda_acid_compatible"],
                   "لكل ملعقة صغيرة بيكنج باودر في كيك أو مافن مناسب: استخدمي "
                   "ربع ملعقة صغيرة بيكربونات ونصف ملعقة صغيرة كريمة التارتار. "
                   "اخلطيها مع المكونات الجافة واتبعي الوصفة.", None),
                  (["only_baking_soda"], "لا تحطين بيكربونات لحالها بدل البيكنج "
                   "باودر؛ ممكن يطلع طعمها واضح. وفّري البديل أو اختاري وصفة مناسبة.", None)]),
            Rule("R19", ["storage_risk"], "storage_warning",
                 "إذا التخزين غير آمن أو غير معروف، السلامة أهم من أي حل.", 100,
                 "🚨 لا تقدمين الأكل قبل ما تتأكدين من سلامة حفظه. "
                 "إذا ما تقدرين تتأكدين، تخلصي منه.",
                 [(["unsafe_storage"], "🚨 التخزين مو آمن؛ لا تذوقين الأكل ولا "
                   "تقدمينه. الأفضل تتخلصين منه.", "DISCARD")],
                 verdict="DO_NOT_SERVE"),
            Rule("R20", ["bottom_burn"], "bottom_burn_assessed",
                 "إذا احتُرق قاع القدر، نفصل الجزء السليم بدون تحريك المحروق.", 80,
                 "طفي النار ولا تحرّكين القاع. انقلي الجزء اللي فوق لقدر نظيف "
                 "بدون كشط الجزء اللاصق والمحروق.",
                 [(["inside_raw"], "🚨 طفي النار وانقلي الجزء غير المحروق "
                   "لقدر نظيف بدون كشط القاع. إذا باقي نيّ، كمّلي استواءه "
                   "قبل التقديم.", "DO_NOT_SERVE")]),
        ]

        # ذاكرة العمل
        self.facts: Set[str] = set()
        self.asked_questions: Set[str] = set()
        self.selected_problem = None
        self.answers = {}
        self.session_id = 0

        # نفس المجالات الأساسية بدون أسئلة تكرر المشكلة المختارة.
        self.categories = {
            "cake": ("🎂 الكيك خرب", ["cake_sank", "cake_dry", "cake_raw_inside"]),
            "sauce": ("🥣 الصوص تخبّص", ["ganache_separated", "ganache_thick", "pastry_cream_thin"]),
            "dough": ("🍞 العجينة عاندت", ["dough_not_rising", "bread_hard"]),
            "taste": ("🧂 الطعم مو مضبوط", ["too_sweet", "too_salty", "too_bitter"]),
            "burn": ("🔥 حرقت الطبخة", ["surface_burn", "bottom_burn", "severe_charring"]),
            "missing": ("🥚 ناقصني مكوّن", ["missing_cream", "missing_egg", "missing_baking_powder"]),
        }
        self.problems = {
            "cake_sank": "الكيك هبط من النص",
            "cake_dry": "الكيك طلع ناشف",
            "cake_raw_inside": "الكيك نيّ من داخل",
            "ganache_separated": "الغاناش انفصل وصار زيتي",
            "ganache_thick": "الغاناش ثقيل مرة",
            "pastry_cream_thin": "كريمة الحلويات ما ثخنت",
            "dough_not_rising": "عجينة الخميرة ما ارتفعت",
            "bread_hard": "الخبز طلع قاسي",
            "too_sweet": "الحلى حالي بزيادة",
            "too_salty": "الطبخة مالحة",
            "too_bitter": "الطعم مرّ",
            "surface_burn": "السطح احترق شوي",
            "bottom_burn": "الطبخة احترقت من تحت",
            "severe_charring": "الأكل تفحّم",
            "missing_cream": "ما عندي كريمة أو قشطة",
            "missing_egg": "ما عندي بيض",
            "missing_baking_powder": "ما عندي بيكنج باودر",
        }

        # الخيارات واضحة؛ سؤال التخزين يسمح بعدم التأكد حفاظًا على السلامة.
        self.questions = {
            "cake_center": ("وسط الكيك وش وضعه؟", [
                ("نيّ أو مثل العجين", "center_raw"), ("مستوي تمام", "inside_fully_cooked")]),
            "cake_baking": ("وش صار وقت الخبز؟", [
                ("خليته زيادة بالفرن", "baked_too_long"),
                ("الوجه غمق قبل ما يستوي الوسط", "outside_dark"),
                ("مشى على وقت الوصفة", "normal_baking")]),
            "raw_time": ("متى انتبهتي إنه نيّ؟", [
                ("توّي مطلعته من الفرن", "just_baked"),
                ("جلس برا أكثر من ساعتين وكان يحتاج تبريد", "unsafe_storage")]),
            "ganache_state": ("الغاناش الحين وش حاله؟", [
                ("بارد ومتكتل", "ganache_cold"), ("دافئ أو بحرارة الغرفة", "ganache_warm")]),
            "ganache_use": ("تبغينه لأي استخدام؟", [
                ("صوص ينصب فوق الحلى", "for_drizzle"),
                ("حشوة أو تغطية تنفرد", "for_spread")]),
            "cream_cooking": ("الكريمة انطبخت لين بدأت تثخن؟", [
                ("لا، شلتها بدري", "insufficient_cooking"),
                ("إيه، بس بعد ما بردت ظلت سائلة", "cream_chilled_thin")]),
            "dough_temp": ("وين خليتي العجينة؟", [
                ("مكان بارد", "environment_cold"), ("مكان دافئ باعتدال", "environment_warm")]),
            "dough_stage": ("العجينة الحين وين وصلت؟", [
                ("لسه ما خبزتها", "still_proofing"), ("خبزتها وطلعت ثقيلة", "already_baked")]),
            "bread_flour": ("زدتي دقيق عن كمية الوصفة؟", [
                ("إيه", "excess_flour"), ("لا", "normal_flour")]),
            "bread_age": ("متى صار الخبز قاسي؟", [
                ("من أول ما طلع من الفرن", "hard_from_oven"),
                ("كان طري وبعدين يبس", "bread_stale")]),
            "sweet_kind": ("وش نوع الحلى؟", [
                ("كيك أو حلى متماسك", "solid_dessert"),
                ("مشروب أو صوص حلو", "sweet_liquid")]),
            "salty_kind": ("وش نوع الطبخة المالحة؟", [
                ("شوربة أو صوص سائل", "liquid_dish"),
                ("رز أو مكرونة", "rice_pasta"), ("طبق ثاني متماسك", "solid_dish")]),
            "taste_dilute": ("تقدرين تزيدين من نفس مكونات الطبخة بدون ملح؟", [
                ("إيه", "unsalted_liquid_compatible"), ("لا", "no_extra_ingredients")]),
            "taste_burn": ("وش أقرب سبب للمرارة؟", [
                ("فيه جزء محترق", "burnt_food"),
                ("من القهوة أو الكاكاو في الحلى", "bitter_cocoa"),
                ("ما فيه احتراق واضح", "other_bitterness")]),
            "burn_inside": ("الجزء اللي ما احترق مستوي؟", [
                ("إيه، مستوي", "inside_fully_cooked"),
                ("لا، باقي نيّ", "inside_raw")]),
            "cream_use": ("الكريمة تبغينها لأي شيء؟", [
                ("صوص طبخ", "creamy_sauce"),
                ("خفق وتزيين", "needs_whipping"),
                ("طبقة لحلى بارد", "cold_dessert")]),
            "cream_sub": ("وش متوفر عندك بدل الكريمة؟", [
                ("حليب كامل الدسم وزبدة", "cream_substitute_compatible"),
                ("زبادي سادة", "have_yogurt"), ("ولا واحد منهم", "no_substitute")]),
            "egg_use": ("البيض ناقص لأي وصفة؟", [
                ("كيك أو مافن بسيط", "simple_cake"),
                ("كاسترد أو ميرنغ", "egg_essential")]),
            "egg_sub": ("وش متوفر عندك بدل البيض؟", [
                ("زبادي سادة", "egg_substitute_compatible"),
                ("موز مهروس", "have_banana"), ("ما عندي بديل", "no_substitute")]),
            "powder_use": ("البيكنج باودر ناقص لأي شيء؟", [
                ("كيك أو مافن سريع", "quick_bread"),
                ("وصفة ثانية", "other_recipe")]),
            "powder_sub": ("وش متوفر عندك؟", [
                ("بيكربونات وكريمة التارتار", "baking_soda_acid_compatible"),
                ("بيكربونات بس", "only_baking_soda"),
                ("ما عندي بديل", "no_substitute")]),
            "safety": ("الأكل ومكوناته محفوظة بشكل آمن؟", [
                ("إيه، متأكدة", "food_safe"),
                ("لا، فيه مشكلة بالتخزين", "unsafe_storage"),
                ("ما أقدر أتأكد من التخزين", "safety_unknown")]),
        }

        self.question_paths = {
            "cake_sank": ["cake_center", "cake_baking"],
            "cake_dry": ["cake_baking"],
            "cake_raw_inside": ["raw_time", "cake_baking"],
            "ganache_separated": ["ganache_state"],
            "ganache_thick": ["ganache_state", "ganache_use"],
            "pastry_cream_thin": ["cream_cooking"],
            "dough_not_rising": ["dough_temp", "dough_stage"],
            "bread_hard": ["bread_flour", "bread_age"],
            "too_sweet": ["sweet_kind"],
            "too_salty": ["salty_kind", "taste_dilute"],
            "too_bitter": ["taste_burn"],
            "surface_burn": ["burn_inside"],
            "bottom_burn": ["burn_inside"],
            "severe_charring": [],
            "missing_cream": ["cream_use", "cream_sub"],
            "missing_egg": ["egg_use", "egg_sub"],
            "missing_baking_powder": ["powder_use", "powder_sub"],
        }

    def select_problem(self, problem: str):
        if problem not in self.problems:
            raise ValueError("المشكلة غير موجودة.")
        self.reset_working_memory()
        self.selected_problem = problem
        self.add_fact(problem)
        # نضيف الحقائق المفهومة من المشكلة نفسها، بدل سؤال المستخدم عنها مرة ثانية.
        basic_facts = {
            "cake_raw_inside": ["center_raw"],
            "ganache_separated": ["ganache", "separated"],
            "ganache_thick": ["ganache", "too_thick"],
            "pastry_cream_thin": ["pastry_cream", "too_thin"],
            "dough_not_rising": ["yeast_dough", "not_rising"],
        }
        self.add_facts(basic_facts.get(problem, []))
        return self.get_questions_for_problem(problem)

    def get_questions_for_problem(self, problem: str):
        if problem not in self.question_paths:
            raise ValueError("المشكلة غير موجودة.")
        questions = list(self.question_paths[problem])
        # البدائل ناقصة قبل الطبخ، والتفحّم الحاد له حكم مباشر؛ ما يحتاجون سؤال حفظ أكل جاهز.
        if not problem.startswith("missing_") and problem != "severe_charring":
            questions.append("safety")
        return [(key, *self.questions[key]) for key in questions]

    def record_choice(self, question_id: str, option_index: int):
        """نحوّل الإجابة إلى حقيقة ونرفض الاختيارات المكررة أو غير الصحيحة."""
        if self.selected_problem is None:
            raise ValueError("اختاري المشكلة أولًا.")
        allowed = {key for key, _, _ in self.get_questions_for_problem(self.selected_problem)}
        if question_id not in allowed:
            raise ValueError("السؤال مو ضمن هالمشكلة.")
        if question_id in self.asked_questions:
            raise ValueError("جاوبتي عن هالسؤال من قبل. ابدئي تحليل جديد لو تبغين تغيّرين الإجابة.")
        if type(option_index) is not int:
            raise ValueError("اختاري رقم صحيح للخيار.")
        options = self.questions[question_id][1]
        if not 0 <= option_index < len(options):
            raise ValueError("الخيار غير موجود.")
        fact = options[option_index][1]
        self.add_fact(fact)
        if fact in {"unsafe_storage", "safety_unknown"}:
            self.add_fact("storage_risk")
        self.asked_questions.add(question_id)
        self.answers[question_id] = option_index
        return True

    def add_fact(self, fact: str):
        self.facts.add(fact)

    def add_facts(self, facts):
        self.facts.update(facts)

    def get_facts(self):
        return self.facts.copy()

    def remove_fact(self, fact: str):
        """Remove a fact when updating working memory programmatically."""
        self.facts.discard(fact)

    def reset_working_memory(self):
        self.facts.clear()
        self.asked_questions.clear()
        self.selected_problem = None
        self.answers.clear()
        self.session_id += 1

    def initialize_facts(self):
        self.reset_working_memory()



class InferenceEngine:
    """Task 2: Forward Chaining + حل التعارض + شرح النتيجة."""
    def __init__(self, rule_base, working_memory):
        # الأعلى أولوية أولًا، وعند التعادل رقم القاعدة الأصغر.
        self.rules = sorted(rule_base, key=lambda r: (-r.priority, int(r.rule_id[1:])))
        self.memory = working_memory
        self.fired_rules = set()
        self.audit_trail = []
        self._session_id = working_memory.session_id

    def run_forward_chaining(self):
        """نشغّل القواعد حسب الأولوية، ونضيف نتائجها للذاكرة حتى ما يبقى تطابق جديد."""
        if self.memory.selected_problem is None:
            raise ValueError("اختاري المشكلة أولًا.")
        if self._session_id != self.memory.session_id:
            self.fired_rules.clear()
            self.audit_trail.clear()
            self._session_id = self.memory.session_id
        questions = self.memory.get_questions_for_problem(self.memory.selected_problem)
        if any(q not in self.memory.asked_questions for q, _, _ in questions):
            raise ValueError("جاوبي عن كل الأسئلة قبل ما تطلبين الحل.")

        # نكرر المرور لأن نتيجة قاعدة ممكن تصبح شرطًا لقاعدة أخرى (R7→R8 وR11→R12).
        while True:
            applicable = next((r for r in self.rules if r.rule_id not in self.fired_rules
                               and r.conditions <= self.memory.facts), None)
            if applicable is None:
                break
            self.memory.add_fact(applicable.conclusion)
            self.fired_rules.add(applicable.rule_id)
            self.audit_trail.append({
                "step": len(self.audit_trail) + 1,
                "rule_id": applicable.rule_id,
                "priority": applicable.priority,
                "matched_premises": sorted(applicable.conditions),
                "inferred_fact": applicable.conclusion,
                "reasoning_string": applicable.description,
            })
            # قاعدة الخطر R19 / التفحم R15 لها الأولوية ولا نكمّل حلول الإنقاذ.
            if applicable.rule_id in {"R15", "R19"}:
                break
        return self.get_result()

    def get_result(self):
        """النصيحة النهائية تأتي من القاعدة الأخيرة التي فُعّلت، لا من دالة حلول منفصلة."""
        if not self.audit_trail:
            raise ValueError("ما لقينا قاعدة مناسبة. راجعي الإجابات.")
        # الحل يجي من آخر قاعدة اشتغلت، بما فيها القاعدة الثانية في سلسلتي R7/R8 وR11/R12.
        active_id = self.audit_trail[-1]["rule_id"]
        rule = next(r for r in self.rules if r.rule_id == active_id)
        message, verdict = rule.choose_advice(self.memory.facts)
        self.audit_trail[-1]["used_for_advice"] = True
        return {
            "verdict": verdict,
            "message": message,
            "winning_rule": active_id,
            "explanation": self.get_explanation(active_id),
            "audit_trail": list(self.audit_trail),
            "inferred_facts": sorted(self.memory.facts),
        }

    def describe_fact(self, fact):
        """نحوّل اسم الشرط البرمجي لعبارة يفهمها المستخدم."""
        names = {
            "ganache": "الغاناش", "separated": "الغاناش منفصل",
            "too_thick": "الغاناش ثقيل", "pastry_cream": "كريمة الحلويات",
            "too_thin": "الكريمة خفيفة", "yeast_dough": "عجينة خميرة",
            "not_rising": "العجينة ما ارتفعت",
            "storage_risk": "التخزين غير آمن أو مو مؤكد",
            "proofing_problem_found": "مشكلة التخمير (استنتاج R7)",
            "salt_problem_found": "زيادة الملح (استنتاج R11)",
            "food_safe": "تم اختيار أن حفظ المكونات آمن",
            "unsalted_liquid_compatible": "ممكن نزيد مكونات بدون ملح",
        }
        if fact in names:
            return names[fact]
        if fact in self.memory.problems:
            return self.memory.problems[fact]
        for _, options in self.memory.questions.values():
            for label, option_fact in options:
                if option_fact == fact:
                    return label
        return fact

    def get_explanation(self, active_id=None):
        """Task 2: نعرض القواعد التي اشتغلت وشروطها المطابقة وسبب كل استنتاج."""
        if not self.audit_trail:
            return "ما انتهى الاستدلال لسه."
        lines = []
        for step in self.audit_trail:
            conditions = " + ".join(self.describe_fact(f) for f in step["matched_premises"])
            lines.append(
                f"{step['step']}. القاعدة {step['rule_id']}\n"
                f"   الشروط المطابقة: {conditions}\n"
                f"   السبب: {step['reasoning_string']}"
            )
        if active_id:
            lines.append(f"🍰 النصيحة من القاعدة {active_id}.")
        return "\n".join(lines)


def create_mama_system():
    system = InteractiveExpertSystem()
    return system, InferenceEngine(system.rules, system)


def analyze_case(problem, answers):
    """نستخدمها لتجربة حالة كاملة بالأسئلة وإرجاع نتيجة الاستدلال."""
    system, engine = create_mama_system()
    system.select_problem(problem)
    for question_id, option_index in answers.items():
        system.record_choice(question_id, option_index)
    return engine.run_forward_chaining()


def run_console():
    """Task 3: واجهة الطرفية، مع رسائل عربية للإدخال الخطأ."""
    system, engine = create_mama_system()
    print("\n🍰 MAMA | ماما — مساعدتك لمشاكل المطبخ")
    for category_id, (name, _) in system.categories.items():
        print(f"  {category_id}: {name}")
    while True:
        category = input("\nاختاري رمز القسم: ").strip()
        if category in system.categories:
            break
        print("القسم مو موجود، جربي مرة ثانية.")
    available = system.categories[category][1]
    for i, problem in enumerate(available, 1):
        print(f"{i}. {system.problems[problem]}")
    while True:
        choice = input("رقم المشكلة: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(available):
            break
        print("اختاري رقم من القائمة، مو حروف.")
    system.select_problem(available[int(choice) - 1])
    for question_id, text, options in system.get_questions_for_problem(system.selected_problem):
        print("\n" + text)
        for i, (label, _) in enumerate(options, 1):
            print(f"{i}. {label}")
        while True:
            choice = input("اختاري رقم الإجابة: ").strip()
            if not choice.isdigit() or not 1 <= int(choice) <= len(options):
                print("اختاري رقم من الخيارات الظاهرة، مو حروف.")
                continue
            system.record_choice(question_id, int(choice) - 1)
            break
    result = engine.run_forward_chaining()
    print("\n🍰 نصيحة ماما:\n" + result["message"])
    print("\nليش ماما قالت كذا؟\n" + result["explanation"])


# ---------------------------------------------------------------------------
# Task 3: reproducible evidence and exhaustive verification (standard library).
# ---------------------------------------------------------------------------
TEST_SCENARIOS = (
    {
        "name": "Test 1 - Salty soup: two-step Forward Chaining",
        "category": "taste",
        "problem": "too_salty",
        "inputs": "taste\n2\n1\n1\n1\n",
        "answers": {"salty_kind": 0, "taste_dilute": 0, "safety": 0},
        "expected_verdict": "FIX",
        "expected_rule": "R12",
        "expected_trace": ["R11", "R12"],
        "expected_validation_messages": 0,
    },
    {
        "name": "Test 2 - Unsafe storage: safety rule overrides rescue",
        "category": "cake",
        "problem": "cake_raw_inside",
        "inputs": "cake\n3\n2\n2\n2\n",
        "answers": {"raw_time": 1, "cake_baking": 1, "safety": 1},
        "expected_verdict": "DISCARD",
        "expected_rule": "R19",
        "expected_trace": ["R19"],
        "expected_validation_messages": 0,
    },
    {
        "name": "Test 3 - Invalid entries: reprompt and recovery",
        "category": "missing",
        "problem": "missing_egg",
        "inputs": "oops\nmissing\nx\n2\n0\n1\n99\n1\n",
        "answers": {"egg_use": 0, "egg_sub": 0},
        "expected_verdict": "FIX",
        "expected_rule": "R16",
        "expected_trace": ["R16"],
        "expected_validation_messages": 4,
    },
)


def run_demo_tests():
    """Run 3 true CLI sessions, then verify verdict/rule/validation behavior."""
    import subprocess
    import sys
    import os

    all_passed = True
    for test in TEST_SCENARIOS:
        completed = subprocess.run(
            [sys.executable, os.path.abspath(__file__)],
            input=test["inputs"], capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
        actual = analyze_case(test["problem"], test["answers"])
        trace = [item["rule_id"] for item in actual["audit_trail"]]
        validation_count = (
            completed.stdout.count("القسم مو موجود، جربي مرة ثانية.")
            + completed.stdout.count("اختاري رقم من القائمة، مو حروف.")
            + completed.stdout.count("اختاري رقم من الخيارات الظاهرة، مو حروف.")
        )
        passed = (
            completed.returncode == 0
            and actual["verdict"] == test["expected_verdict"]
            and actual["winning_rule"] == test["expected_rule"]
            and trace == test["expected_trace"]
            and validation_count == test["expected_validation_messages"]
            and f"القاعدة {test['expected_rule']}" in completed.stdout
        )
        all_passed &= passed
        print("\n" + "=" * 68)
        print(test["name"])
        print("=" * 68)
        print(completed.stdout)
        print(f"Verdict: {actual['verdict']} | Final rule: {actual['winning_rule']}")
        print(f"Fired rules: {', '.join(trace)} | Input errors handled: {validation_count}")
        print("PASS" if passed else "FAIL")
    return all_passed


def run_self_test():
    """Explore every permitted answer combination for all 17 problems."""
    import itertools

    ref, _ = create_mama_system()
    coverage = set()
    tested = 0
    assert len(ref.rules) == 20
    assert len(ref.problems) == 17
    for problem in ref.problems:
        paths = ref.get_questions_for_problem(problem)
        choice_ranges = [range(len(options)) for _, _, options in paths]
        for choices in itertools.product(*choice_ranges):
            system, engine = create_mama_system()
            system.select_problem(problem)
            for (question_id, _, _), choice in zip(paths, choices):
                system.record_choice(question_id, choice)
            result = engine.run_forward_chaining()
            assert result["winning_rule"] == result["audit_trail"][-1]["rule_id"]
            assert result["explanation"] and result["message"]
            assert all(step["matched_premises"] for step in result["audit_trail"])
            # A food-storage concern always takes precedence over a rescue.
            if "storage_risk" in system.facts:
                assert result["winning_rule"] == "R19", (problem, choices)
            coverage.update(step["rule_id"] for step in result["audit_trail"])
            tested += 1
    expected = {f"R{i}" for i in range(1, 21)}
    assert coverage == expected, f"Uncovered rules: {sorted(expected - coverage)}"
    print(f"PASS: {tested} possible answer combinations, 17 problems, "
          f"{len(coverage)}/20 rules covered.")
    return True


if __name__ == "__main__":
    import sys

    try:
        if len(sys.argv) == 1:
            run_console()
        elif sys.argv[1:] == ["--demo-tests"]:
            sys.exit(0 if run_demo_tests() else 1)
        elif sys.argv[1:] == ["--self-test"]:
            sys.exit(0 if run_self_test() else 1)
        else:
            print("Usage: python main.py [--demo-tests | --self-test]")
            sys.exit(2)
    except (KeyboardInterrupt, EOFError):
        print("\nتم إيقاف الجلسة بدون حفظ أي بيانات.")
        sys.exit(0)
