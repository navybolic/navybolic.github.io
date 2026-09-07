#!/usr/bin/env python3
"""Copy ChatGPT bank (untouched source) and append 15 new CAP-X items."""
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path("/home/workdir/artifacts/cap-x-trainer")
SRC = ROOT / "data" / "chatgpt_bank_backup.json"
OUT = ROOT / "data" / "questions.json"

OFFICIAL = "https://www.certifiedanalytics.org/cap-expert"
RESOURCES = "https://www.certifiedanalytics.org/exam-resources"
FRAMEWORK = "https://drive.google.com/file/d/14iRGcKL7mu7fm6XFcx3NzRVfGDH01kzY/view"
ABOK = {
    "1": "https://drive.google.com/file/d/1xpZ78WiaYsZ4F6J44ahMoqrmN2RYGV3x/view",
    "2": "https://drive.google.com/file/d/1W1eIPDgroLTY9bZJ3N0O3_3V5LHkhxT2/view",
    "3": "https://drive.google.com/file/d/1AAad156Wsd8KdrscDpzxkyJSZ4zDvhC9/view",
    "4": "https://drive.google.com/file/d/1EJ0ItOQSJ821dy9bZl8ERiAb-X9M6-Sq/view",
    "5": "https://drive.google.com/file/d/1yyHXRUacIUJdwY3fbykUB-e_DtAAlezt/view",
    "6": "https://drive.google.com/file/d/1YLpRg9RUE-tha3Jkxu8U2qFRXCD07Gew/view",
    "7": "https://drive.google.com/file/d/1y67xnqWTD_-xHW1t_AneCyFB8mzDkWDG/view",
    "8": "https://drive.google.com/file/d/13v4WCaewlo67GWw0uyajVfCm7Nk2BmhG/view",
}


def C(source, url, locator):
    return {"source": source, "url": url, "locator": locator}


def Q(**kwargs):
    return kwargs


NEW = [
    Q(
        question_id="CAPX-D1-Q101", revision=1, status="eligible", domain="I",
        objectives=["CAP-X Domain I"], topic="Scope and constraints",
        section="Business Problem Framing", difficulty="moderate",
        stem="A vice president asks analytics to 'optimize the entire supply network this quarter.' Transportation, inventory, and supplier-capacity data are incomplete for two regions, and a labor contract freeze blocks changing shift patterns until next year. What should the team do first?",
        correct_key="C",
        options=[
            {"key": "A", "text": "Accept the enterprise-wide scope and assemble every available supply-chain table so modeling can start immediately.", "is_correct": False,
             "rationale": "An unconstrained slogan is not a problem statement. Known policy and data limits must be written into scope before data wrangling becomes the project.",
             "citations": [C("CAP-Expert Domain I", OFFICIAL, "Evaluate the scope of the business problem"), C("ABOK CH2", ABOK["2"], "Target problem and constraints")]},
            {"key": "B", "text": "Refuse the request because incomplete data means no analytics work is possible.", "is_correct": False,
             "rationale": "Data gaps are constraints to disclose and manage. Scope can shrink to a decision the current data and contract allow.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Identify needed and available data"), C("ABOK CH3", ABOK["3"], "Fitness for use")]},
            {"key": "C", "text": "Rewrite the request as a time-bounded decision with explicit geographies, frozen labor rules, success metrics, and sponsor-accepted data gaps.", "is_correct": True,
             "rationale": "Domain I requires a usable business problem: outcome, scope, constraints, and measures. Contract and data limits belong in that statement before methods are chosen.",
             "citations": [C("CAP-Expert Domain I", OFFICIAL, "Understanding the business problem and evaluating its scope"), C("ABOK CH2", ABOK["2"], "Getting started with the target problem")]},
            {"key": "D", "text": "Select a network-optimization solver first so the scope discussion has a technical anchor.", "is_correct": False,
             "rationale": "Methodology selection is Domain IV and follows a framed problem. A solver does not define the decision, horizon, or constraint set.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Methodology selection follows framing"), C("ABOK CH5", ABOK["5"], "Methodology selection")]},
        ],
    ),
    Q(
        question_id="CAPX-D1-Q102", revision=1, status="eligible", domain="I",
        objectives=["CAP-X Domain I"], topic="Conflicting success measures",
        section="Business Problem Framing", difficulty="advanced",
        stem="Finance wants the project scored on contribution margin. Operations wants it scored on on-time fill rate. Both groups can block deployment. The sponsor says 'just pick one KPI so we can start.' What is the most appropriate response?",
        correct_key="B",
        options=[
            {"key": "A", "text": "Adopt contribution margin because finance controls the budget.", "is_correct": False,
             "rationale": "Budget authority is not identical to the decision the model must support. Ignoring operations produces a metric operators will not use.",
             "citations": [C("CAP-Expert Domain I", OFFICIAL, "Stakeholders and problem ownership"), C("INFORMS Analytics Framework", FRAMEWORK, "Business problem framing tasks")]},
            {"key": "B", "text": "Document both outcomes, how they conflict, the decision each would change, and a sponsor-approved primary measure plus a monitored constraint.", "is_correct": True,
             "rationale": "Expert framing records the trade-off instead of hiding it. One primary decision metric plus a watched constraint keeps deployment politically and operationally viable.",
             "citations": [C("CAP-Expert Domain I", OFFICIAL, "Success measures and scope"), C("ABOK CH2", ABOK["2"], "Stakeholders and target problem")]},
            {"key": "C", "text": "Build two independent models and let each function deploy its own score.", "is_correct": False,
             "rationale": "Two unreconciled production scores encode the conflict and leave no single lifecycle owner.",
             "citations": [C("CAP-Expert Domain VII", OFFICIAL, "Lifecycle ownership of a solution"), C("ABOK CH8", ABOK["8"], "Deployment and life cycle")]},
            {"key": "D", "text": "Replace both KPIs with a model-fit statistic so the debate becomes technical.", "is_correct": False,
             "rationale": "Fit statistics are not business outcomes and cannot settle a value conflict between margin and service.",
             "citations": [C("CAP-Expert Domain I vs V", OFFICIAL, "Business measures precede model-quality measures"), C("ABOK CH6", ABOK["6"], "Communicating model findings")]},
        ],
    ),
    Q(
        question_id="CAPX-D2-Q101", revision=1, status="eligible", domain="II",
        objectives=["CAP-X Domain II"], topic="Translating a business question into an analytics problem",
        section="Analytics Problem Framing", difficulty="moderate",
        stem="A retailer wants to 'know which stores will miss plan next month' so regional managers can pre-position inventory. Which statement is the best analytics-problem framing?",
        correct_key="A",
        options=[
            {"key": "A", "text": "Predict, at store-SKU-week grain, P(miss plan) and expected unit shortfall in time for a weekly replenishment decision, subject to current lead times.", "is_correct": True,
             "rationale": "A good analytics frame names the decision, grain, output, horizon, and operating constraint. That is Domain II, not a restatement of the slogan.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Frame the business question as an analytics problem"), C("ABOK CH2", ABOK["2"], "From business question to analytics problem")]},
            {"key": "B", "text": "Cluster stores on last year's sales so similar stores can share a single forecast.", "is_correct": False,
             "rationale": "Clustering may be a later method. It does not define the prediction target, decision, or timing the managers need.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Methods are chosen after the analytics problem is stated"), C("ABOK CH5", ABOK["5"], "Methodology selection")]},
            {"key": "C", "text": "Report last month's miss-plan rate by region as the analytics solution.", "is_correct": False,
             "rationale": "A rear-view report does not support a next-month pre-positioning decision.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Analytics outputs must serve the stated decision"), C("ABOK CH4", ABOK["4"], "Descriptive vs predictive purpose")]},
            {"key": "D", "text": "Wait until a complete SKU master exists in every region before framing the problem.", "is_correct": False,
             "rationale": "Data completeness is assessed inside the framed problem. Framing first tells you which completeness gaps actually matter.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Identify data needed after the analytics question is framed"), C("ABOK CH3", ABOK["3"], "Data requirements follow the question")]},
        ],
    ),
    Q(
        question_id="CAPX-D2-Q102", revision=1, status="eligible", domain="II",
        objectives=["CAP-X Domain II"], topic="Assumptions and reformulation",
        section="Analytics Problem Framing", difficulty="advanced",
        stem="An analytics problem is framed as a linear program that assumes demand is known. Midway through scoping, demand owners say next-quarter volume is highly uncertain and leadership will not lock a single number. What should the team do?",
        correct_key="D",
        options=[
            {"key": "A", "text": "Keep the LP and replace demand with last year's actuals so the math stays tractable.", "is_correct": False,
             "rationale": "Silent substitution of a stale point estimate hides the uncertainty the decision makers just declared material.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "State assumptions and reformulate when they fail"), C("ABOK CH5", ABOK["5"], "Prescriptive models and uncertain inputs")]},
            {"key": "B", "text": "Abandon analytics because uncertainty means optimization is invalid.", "is_correct": False,
             "rationale": "Uncertainty changes the formulation; it does not cancel the decision. Stochastic, robust, or scenario formulations exist for this case.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Select methods that match the problem structure"), C("ABOK CH5", ABOK["5"], "Stochastic and robust alternatives")]},
            {"key": "C", "text": "Fit a demand-forecast model and treat its point forecast as certain inside the original LP.", "is_correct": False,
             "rationale": "A point forecast is still one number. If leadership will not lock a single volume, the analytics problem itself must carry uncertainty into the recommendation.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Outputs must match how the decision will be used"), C("ABOK CH6", ABOK["6"], "Communicating uncertainty")]},
            {"key": "D", "text": "Reformulate: treat demand as uncertain, define scenarios or a distribution with the demand owners, and change the recommendation from one plan to a policy or robust plan they can act on.", "is_correct": True,
             "rationale": "Domain II includes restating the analytics problem when a governing assumption dies. The output type should match a decision under uncertainty.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Reformulate the analytics problem as understanding changes"), C("ABOK CH2", ABOK["2"], "Analytics problem framing and assumptions")]},
        ],
    ),
    Q(
        question_id="CAPX-D2-Q103", revision=1, status="eligible", domain="II",
        objectives=["CAP-X Domain II"], topic="Success metrics for the analytics problem",
        section="Analytics Problem Framing", difficulty="moderate",
        stem="A credit team wants a model that 'improves collections.' After interviews, the operational decision is: which delinquent accounts a 12-person desk should call tomorrow. Which analytics success metric is most aligned?",
        correct_key="B",
        options=[
            {"key": "A", "text": "Area under the ROC curve on a random 30% holdout of all accounts.", "is_correct": False,
             "rationale": "AUC on a random split ignores capacity (12 people) and the tomorrow decision. Ranking quality is not the business action.",
             "citations": [C("CAP-Expert Domain II and V", OFFICIAL, "Metrics must reflect the decision, not only discrimination"), C("ABOK CH6", ABOK["6"], "Evaluating models against the decision")]},
            {"key": "B", "text": "Dollars collected from the 12 × next-day call list versus the current ranking policy, on a time-aware test set.", "is_correct": True,
             "rationale": "The metric is the value of the actual decision under the real capacity constraint, evaluated without leakage from the future.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Define analytics success in decision terms"), C("ABOK CH6", ABOK["6"], "Business evaluation of model output")]},
            {"key": "C", "text": "Training-set accuracy of a 50% probability cutoff.", "is_correct": False,
             "rationale": "Training accuracy is optimistic and a default cutoff ignores desk capacity and dollars at risk.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Do not treat training fit as success"), C("ABOK CH6", ABOK["6"], "Overfitting and improper metrics")]},
            {"key": "D", "text": "Number of features the model uses, minimized for interpretability.", "is_correct": False,
             "rationale": "Parsimony can be a constraint, not the objective. Fewer features does not mean better collections.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Objectives vs constraints"), C("ABOK CH5", ABOK["5"], "Interpretability as a design constraint")]},
        ],
    ),
    Q(
        question_id="CAPX-D3-Q101", revision=1, status="eligible", domain="III",
        objectives=["CAP-X Domain III"], topic="Data needed versus data available",
        section="Data", difficulty="moderate",
        stem="A hospital length-of-stay model needs admission hour, care-pathway, and discharge disposition. Admission hour is reliably captured. Pathway is in free-text notes. Disposition is missing for 40% of stays from one campus. What is the best next data action?",
        correct_key="C",
        options=[
            {"key": "A", "text": "Drop the campus with missing disposition so the remaining table is complete.", "is_correct": False,
             "rationale": "Dropping a campus silently changes the population and can hide a site-specific process the model is supposed to support.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Document data limitations and population coverage"), C("ABOK CH3", ABOK["3"], "Missingness and selection")]},
            {"key": "B", "text": "Impute every missing disposition with the system-wide mode and proceed to modeling.", "is_correct": False,
             "rationale": "Mode imputation on a campus-structured 40% hole invents a clinical event and conceals a data-generation problem.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Manipulate data so it is usable — without fabricating the target process"), C("ABOK CH3", ABOK["3"], "Missing data handling")]},
            {"key": "C", "text": "Profile the missingness with campus operations, decide whether disposition can be recovered or must become a documented limitation, and only then choose an analysis population.", "is_correct": True,
             "rationale": "Domain III is identify, assess, and document. Missingness that is structural must be understood with data owners before transformation or exclusion.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Identify needed vs available data and document gaps"), C("ABOK CH3", ABOK["3"], "Data quality and documentation")]},
            {"key": "D", "text": "Replace pathway notes and disposition with a purchased socioeconomic overlay because it is complete.", "is_correct": False,
             "rationale": "External completeness does not substitute for the clinical fields the decision needs. Convenience data is not fitness for use.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Fitness for the analytics problem, not mere completeness"), C("ABOK CH3", ABOK["3"], "Relevant data vs available data")]},
        ],
    ),
    Q(
        question_id="CAPX-D3-Q102", revision=1, status="eligible", domain="III",
        objectives=["CAP-X Domain III"], topic="Leakage and time validity",
        section="Data", difficulty="advanced",
        stem="A churn model will be scored on Friday for customers who might cancel next month. A proposed feature is 'total tickets closed in the next 30 days.' What is the correct treatment?",
        correct_key="A",
        options=[
            {"key": "A", "text": "Exclude it. At score time those tickets have not happened; using them is leakage and the model cannot be deployed as designed.", "is_correct": True,
             "rationale": "Features must be available at decision time. Future tickets are information the Friday job will not have.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Data must be usable for the decision timing"), C("ABOK CH3", ABOK["3"], "Temporal validity of features")]},
            {"key": "B", "text": "Keep it; any variable that raises AUC in cross-validation is admissible.", "is_correct": False,
             "rationale": "Cross-validation can reward leakage. Deployability, not peak AUC, governs feature eligibility.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Evaluation must reflect deployment conditions"), C("ABOK CH6", ABOK["6"], "Honest validation")]},
            {"key": "C", "text": "Keep it in training but drop it only if production monitoring shows drift.", "is_correct": False,
             "rationale": "The defect is logical, not a later drift issue. The feature is undefined at score time.",
             "citations": [C("CAP-Expert Domain VII", OFFICIAL, "Monitoring does not excuse an invalid feature"), C("ABOK CH8", ABOK["8"], "Lifecycle cannot repair leakage")]},
            {"key": "D", "text": "Replace ticket counts with the customer's account number because identifiers are safer.", "is_correct": False,
             "rationale": "An identifier is not a substitute feature and can introduce other leakage or fairness problems.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Choose data that represents the process, not an ID"), C("ABOK CH3", ABOK["3"], "Appropriate attributes")]},
        ],
    ),
    Q(
        question_id="CAPX-D3-Q103", revision=1, status="eligible", domain="III",
        objectives=["CAP-X Domain III"], topic="Documentation and lineage",
        section="Data", difficulty="moderate",
        stem="Two analysts produce different monthly revenue totals from 'the same warehouse table.' Leadership asks which number is official. What documentation closes the gap fastest?",
        correct_key="B",
        options=[
            {"key": "A", "text": "A slide with both totals and a request to 'use the average.'", "is_correct": False,
             "rationale": "Averaging unexplained extracts creates a third unofficial number and no lineage.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Required documentation and reporting"), C("ABOK CH3", ABOK["3"], "Data documentation")]},
            {"key": "B", "text": "A data dictionary plus extract logic: grain, filters, as-of timestamp, inclusion of returns/tax, and the job that built each extract.", "is_correct": True,
             "rationale": "Domain III expects documentation that makes a number reconstructable: definition, timing, transformation, and owner.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Documentation and reporting needs"), C("ABOK CH3", ABOK["3"], "Lineage and definitions")]},
            {"key": "C", "text": "The machine-learning code that later consumes the table.", "is_correct": False,
             "rationale": "Model code does not define the business extract. The conflict is upstream of modeling.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Model code ≠ data definition"), C("ABOK CH6", ABOK["6"], "Separate data prep documentation")]},
            {"key": "D", "text": "An email from the warehouse vendor confirming uptime was 99.9%.", "is_correct": False,
             "rationale": "Infrastructure availability does not reconcile two different business rules.",
             "citations": [C("CAP-Expert Domain III", OFFICIAL, "Quality of definition, not only system uptime"), C("ABOK CH3", ABOK["3"], "Data quality dimensions")]},
        ],
    ),
    Q(
        question_id="CAPX-D4-Q101", revision=1, status="eligible", domain="IV",
        objectives=["CAP-X Domain IV"], topic="Matching method to problem type",
        section="Methodology Selection", difficulty="moderate",
        stem="The decision is: set next week's production quantity for 200 SKUs to meet uncertain demand at minimum expected cost plus shortage penalty, with known capacities. Which approach is the best first selection?",
        correct_key="C",
        options=[
            {"key": "A", "text": "k-means clustering of SKUs by color and brand.", "is_correct": False,
             "rationale": "Clustering does not produce a feasible production quantity under capacity and cost.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Select methods that can answer the framed problem"), C("ABOK CH5", ABOK["5"], "Matching methods to problem type")]},
            {"key": "B", "text": "A deep neural net trained to classify whether a SKU is 'hot' or 'not.'", "is_correct": False,
             "rationale": "A binary label is not a production plan and ignores capacity and shortage cost.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Tools must enable the solution, not merely classify"), C("ABOK CH5", ABOK["5"], "Predictive vs prescriptive")]},
            {"key": "C", "text": "A prescriptive inventory/production model (newsvendor or stochastic program) that uses a demand distribution and explicit capacities and costs.", "is_correct": True,
             "rationale": "The framed problem is a resource decision under uncertainty with costs and constraints — a prescriptive model is the matching family.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Select methods, techniques, and tools for the problem"), C("ABOK CH5", ABOK["5"], "Prescriptive analytics under uncertainty")]},
            {"key": "D", "text": "A word cloud of customer reviews about the 200 SKUs.", "is_correct": False,
             "rationale": "Unstructured visualization does not yield a feasible weekly quantity.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Method must be capable of the required output"), C("ABOK CH4", ABOK["4"], "Descriptive methods and their limits")]},
        ],
    ),
    Q(
        question_id="CAPX-D4-Q102", revision=1, status="eligible", domain="IV",
        objectives=["CAP-X Domain IV"], topic="Tool and software choice",
        section="Methodology Selection", difficulty="moderate",
        stem="A regulated insurer must produce an explainable rate-change recommendation that internal actuaries can reproduce after staff turnover. A vendor demo shows a black-box model with slightly higher validation lift. What should guide the selection?",
        correct_key="D",
        options=[
            {"key": "A", "text": "Always choose the higher-lift vendor model; lift is the only CAP-relevant criterion.", "is_correct": False,
             "rationale": "Domain IV includes constraints: explainability, reproducibility, skills, and governance — not lift alone.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Software and tools that enable the solution under constraints"), C("ABOK CH5", ABOK["5"], "Practical constraints on method choice")]},
            {"key": "B", "text": "Choose spreadsheets only, because they are inherently auditable.", "is_correct": False,
             "rationale": "Spreadsheets can be opaque and fragile. Auditability comes from documented logic and control, not from the file type.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Tools must support control and reproduction"), C("ABOK CH8", ABOK["8"], "Lifecycle and maintainability")]},
            {"key": "C", "text": "Postpone selection until a tool is found that needs no human actuary.", "is_correct": False,
             "rationale": "Staff-out-of-the-loop is not a stated requirement and conflicts with regulated review.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Deployment includes the operating model and people"), C("ABOK CH8", ABOK["8"], "People in deployment")]},
            {"key": "D", "text": "Prefer a method and toolchain actuaries can explain, reproduce, and maintain, even if lift is slightly lower, and record the lift trade-off for the sponsor.", "is_correct": True,
             "rationale": "Method selection is multi-criteria: decision quality, constraints, skills, and lifecycle. Transparency and reproducibility are binding here.",
             "citations": [C("CAP-Expert Domain IV", OFFICIAL, "Select methods and tools that the organization can run"), C("ABOK CH5", ABOK["5"], "Methodology selection under organizational constraints")]},
        ],
    ),
    Q(
        question_id="CAPX-D5-Q101", revision=1, status="eligible", domain="V",
        objectives=["CAP-X Domain V"], topic="Calibration and communicating findings",
        section="Model Development", difficulty="moderate",
        stem="A risk model’s predicted 10% default band experiences 22% defaults in a recent out-of-time slice. Business users treat 10% as a pricing input. What is the most appropriate development action?",
        correct_key="B",
        options=[
            {"key": "A", "text": "Ship the model; ranking quality (AUC) is still acceptable.", "is_correct": False,
             "rationale": "If users consume probabilities as prices, miscalibration is a business defect even when rank-order is fine.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Calibrate and communicate model findings"), C("ABOK CH6", ABOK["6"], "Calibration vs discrimination")]},
            {"key": "B", "text": "Investigate the shift, recalibrate or rebuild so reported probabilities match observed rates on a time-respecting test, and show users the before/after reliability plot.", "is_correct": True,
             "rationale": "Domain V includes calibration and communication. Users acting on 10% need a probability that means 10% under current conditions.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Identify, calibrate, and communicate findings"), C("ABOK CH6", ABOK["6"], "Model assessment and communication")]},
            {"key": "C", "text": "Multiply every score by 2.2 in production without analysis.", "is_correct": False,
             "rationale": "A global fudge factor without diagnosing mix shift or population change is not calibration discipline.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Calibration is an analyzed step, not a patch"), C("ABOK CH6", ABOK["6"], "Responsible adjustment")]},
            {"key": "D", "text": "Convert the model to a pass/fail flag so probabilities are no longer shown.", "is_correct": False,
             "rationale": "Hiding the number does not fix a model the process still uses for pricing unless the decision itself changes.",
             "citations": [C("CAP-Expert Domain II", OFFICIAL, "Output type must still match the decision"), C("ABOK CH2", ABOK["2"], "Analytics outputs")]},
        ],
    ),
    Q(
        question_id="CAPX-D5-Q102", revision=1, status="eligible", domain="V",
        objectives=["CAP-X Domain V"], topic="Validation design",
        section="Model Development", difficulty="advanced",
        stem="A demand model will be retrained monthly and used to order parts with a six-week lead time. Which validation design best matches that use?",
        correct_key="A",
        options=[
            {"key": "A", "text": "Walk-forward (rolling origin) evaluation at the monthly cadence, scoring a six-week horizon each fold, with error reported in units and dollars.", "is_correct": True,
             "rationale": "Validation must mimic retrain frequency and the lead-time horizon the order decision actually faces.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Build and evaluate the model under intended use"), C("ABOK CH6", ABOK["6"], "Time-series / operational validation")]},
            {"key": "B", "text": "A single random 80/20 split of weeks, shuffled.", "is_correct": False,
             "rationale": "Shuffling weeks leaks future patterns into training and ignores lead time.",
             "citations": [C("CAP-Expert Domain III and V", OFFICIAL, "Respect time in data and evaluation"), C("ABOK CH6", ABOK["6"], "Invalid splits")]},
            {"key": "C", "text": "Optimize only in-sample R² and stop.", "is_correct": False,
             "rationale": "In-sample fit is not evidence the monthly six-week order will work.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Evaluation against intended use"), C("ABOK CH6", ABOK["6"], "Overfitting")]},
            {"key": "D", "text": "Ask the vendor for a marketing case study from another industry.", "is_correct": False,
             "rationale": "External anecdotes are not a validation design for this series, horizon, or cost structure.",
             "citations": [C("CAP-Expert Domain V", OFFICIAL, "Findings must be produced for this model"), C("Exam resources", RESOURCES, "Blueprint: model development tasks")]},
        ],
    ),
    Q(
        question_id="CAPX-D6-Q101", revision=1, status="eligible", domain="VI",
        objectives=["CAP-X Domain VI"], topic="Deployment into the business process",
        section="Deployment", difficulty="moderate",
        stem="A well-validated staffing model sits in a data-science repository. Frontline supervisors still build the weekly roster in a spreadsheet and have never seen the model output. What is the deployment gap?",
        correct_key="C",
        options=[
            {"key": "A", "text": "There is no gap; repository storage is deployment.", "is_correct": False,
             "rationale": "Deployment means the solution is in the business process that makes the decision, not merely in a code repo.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Deliver the analytics solution into the business"), C("ABOK CH8", ABOK["8"], "Deployment vs development")]},
            {"key": "B", "text": "The only gap is that AUC is not printed on the roster.", "is_correct": False,
             "rationale": "A model-quality statistic on a report does not put recommendations into the roster workflow.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Integration with the operating process"), C("ABOK CH8", ABOK["8"], "Use of results")]},
            {"key": "C", "text": "The model is not embedded in the roster workflow with owners, timing, fallback, and training for supervisors.", "is_correct": True,
             "rationale": "Domain VI is delivery into the business: process, people, timing, and exception paths — not just an artifact.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Delivering the solution into the business"), C("ABOK CH8", ABOK["8"], "Organizational deployment")]},
            {"key": "D", "text": "Deployment is complete once Legal has approved the algorithm in principle.", "is_correct": False,
             "rationale": "Legal review can be necessary but is not the same as operational use.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Operational delivery, not only approval"), C("ABOK CH8", ABOK["8"], "Go-live conditions")]},
        ],
    ),
    Q(
        question_id="CAPX-D6-Q102", revision=1, status="eligible", domain="VI",
        objectives=["CAP-X Domain VI"], topic="Change management and fallback",
        section="Deployment", difficulty="advanced",
        stem="On go-live week the scoring job fails at 4 a.m. and cannot be rerun before the 6 a.m. dispatch cutoff. What deployment design should already exist?",
        correct_key="A",
        options=[
            {"key": "A", "text": "A documented fallback (last good plan, rules, or manual protocol), an owner on call, and a communication path to dispatch.", "is_correct": True,
             "rationale": "Deployment includes failure modes. A cutoff-driven process needs a rehearsed degraded mode, not heroics.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Deliver a runnable business process, including exceptions"), C("ABOK CH8", ABOK["8"], "Operational readiness")]},
            {"key": "B", "text": "An email to the data-science team after dispatch ends, asking them to look Monday.", "is_correct": False,
             "rationale": "After-the-fact notice does not protect the 6 a.m. decision.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "Timing of the solution in the business calendar"), C("ABOK CH8", ABOK["8"], "Service levels")]},
            {"key": "C", "text": "A plan to retrain the model from scratch during the outage.", "is_correct": False,
             "rationale": "Retraining is not an incident fallback and will miss the cutoff.",
             "citations": [C("CAP-Expert Domain V vs VI", OFFICIAL, "Retrain is development; dispatch is operations"), C("ABOK CH8", ABOK["8"], "Run vs rebuild")]},
            {"key": "D", "text": "Silence; failed jobs should not influence humans.", "is_correct": False,
             "rationale": "The business still dispatches. No output is itself a process failure that needs a designed response.",
             "citations": [C("CAP-Expert Domain VI", OFFICIAL, "The business process continues and must be designed for"), C("ABOK CH8", ABOK["8"], "Exception handling")]},
        ],
    ),
    Q(
        question_id="CAPX-D7-Q101", revision=1, status="eligible", domain="VII",
        objectives=["CAP-X Domain VII"], topic="Lifecycle monitoring and retraining",
        section="Lifecycle Management", difficulty="moderate",
        stem="Six months after deployment, a pricing model's average predicted conversion is unchanged, but actual conversion in one channel has dropped by half. What is the most appropriate lifecycle action?",
        correct_key="C",
        options=[
            {"key": "A", "text": "Do nothing; predicted conversion is stable so the model is healthy.", "is_correct": False,
             "rationale": "Stability of the prediction is not stability of the world. Outcome drift with flat predictions is a monitoring alert.",
             "citations": [C("CAP-Expert Domain VII", OFFICIAL, "Ongoing oversight and calibration"), C("ABOK CH8", ABOK["8"], "Performance monitoring")]},
            {"key": "B", "text": "Retrain immediately on all historical data including the broken channel without diagnosis.", "is_correct": False,
             "rationale": "Blind retrain can bake a broken process into the model. Diagnose first (process change, tracking bug, mix shift).",
             "citations": [C("CAP-Expert Domain VII", OFFICIAL, "Oversight before recalibration"), C("ABOK CH8", ABOK["8"], "When to retrain")]},
            {"key": "C", "text": "Raise a monitoring incident: compare feature and outcome drift by channel, check logging and process changes, then recalibrate, retrain, or retire the channel policy with an owner.", "is_correct": True,
             "rationale": "Lifecycle management is detect, diagnose, act, and assign ownership — not a single reflex.",
             "citations": [C("CAP-Expert Domain VII", OFFICIAL, "Oversight, calibration, and training over the life of the solution"), C("ABOK CH8", ABOK["8"], "Model life cycle management")]},
            {"key": "D", "text": "Delete the monitoring dashboard so leadership is not alarmed.", "is_correct": False,
             "rationale": "Hiding drift is the opposite of lifecycle control.",
             "citations": [C("CAP-Expert Domain VII", OFFICIAL, "Ongoing oversight"), C("Exam resources", RESOURCES, "Lifecycle domain weight and intent")]},
        ],
    ),
]


def normalize(q):
    """Ensure ChatGPT items have the same citation shape the player expects."""
    q = deepcopy(q)
    for opt in q.get("options", []):
        new_cites = []
        for c in opt.get("citations") or []:
            new_cites.append({
                "source": c.get("source") or c.get("source_file") or c.get("section_heading") or "Source",
                "url": c.get("url") or c.get("drive_url") or c.get("external_locator") or "",
                "locator": c.get("locator") or c.get("section_heading") or c.get("section")
                or ("pp. %s–%s" % (c["printed_page_start"], c["printed_page_end"])
                    if c.get("printed_page_start") else ""),
            })
        opt["citations"] = new_cites
    q.setdefault("section", q.get("topic") or "")
    q.setdefault("objectives", [])
    return q


def main():
    with open(SRC) as f:
        bank = json.load(f)
    questions = [normalize(q) for q in bank["questions"]]
    seen = {q["question_id"] for q in questions}
    for q in NEW:
        if q["question_id"] in seen:
            raise SystemExit("duplicate " + q["question_id"])
        questions.append(q)
        seen.add(q["question_id"])
    from collections import Counter
    counts = Counter(q["domain"] for q in questions)
    out = {
        "bank_id": "CAP-X-TRAINER-2026-09-07",
        "bank_version": "1.1.0",
        "source_snapshot_date": "2026-09-07",
        "blueprint": "CAP-Expert (CAP-X) INFORMS Analytics Framework seven domains",
        "question_count": len(questions),
        "domain_counts": {k: counts[k] for k in ["I", "II", "III", "IV", "V", "VI", "VII"]},
        "notes": "Original 100 items copied from ChatGPT CAP Exam Coach bank; 15 trainer-authored items appended. Original Drive files were not modified.",
        "form_size": 115,
        "form_domain_targets": {"I": 18, "II": 20, "III": 24, "IV": 15, "V": 18, "VI": 12, "VII": 8},
        "questions": questions,
    }
    OUT.write_text(json.dumps(out, indent=2))
    print("wrote", OUT, "n=", out["question_count"], "domains", out["domain_counts"])


if __name__ == "__main__":
    main()
