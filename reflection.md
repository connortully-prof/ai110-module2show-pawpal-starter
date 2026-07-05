# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial design used a simple object-oriented structure with an Owner, Pet, Task, PlannedTask, DailyPlan, and DailyPlanScheduler. The owner and pet hold basic profile information, tasks represent care activities with a duration and priority, and the scheduler turns those tasks into a daily plan.
- I assigned each class a clear responsibility: the owner and pet store user and pet details, tasks describe the work to be scheduled, and the scheduler decides which tasks fit within the available time and explains why.

**b. Design changes**

- The main design change was keeping the implementation simple by focusing on a single scheduling rule: sort by priority and include tasks that fit the remaining time. I did not add more complex features like recurring tasks or time slots during the first version because the core objective was to make the planner work reliably.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers available time and task priority. It also uses the task duration as a constraint, since each task must fit into the remaining daily time budget.
- I decided that time and priority were the most important constraints because the app is meant to help a busy owner make a practical daily plan quickly. A simple priority-based approach makes the results easy to understand and test.

**b. Tradeoffs**

- One tradeoff is that the scheduler only checks for exact time matches when detecting conflicts, rather than handling overlapping durations. This keeps the logic lightweight and easy to understand while still warning the owner about obvious clashes.
- This tradeoff is reasonable for this project because the goal is to create a clear first version of the planner rather than a full-time scheduling engine.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI tools to help design the class structure, generate the initial scheduler code, build the Streamlit UI, debug test issues, and draft the final reflection and documentation. The most effective features were code generation, test suggestions, and quick debugging help when the app or tests failed.
- The most useful prompts were requests for implementation steps, test cases, and suggestions for improving readability in the scheduler logic.

**b. Judgment and verification**

- One example was when the AI suggested a more compact version of the conflict detection logic. I modified it to keep the implementation clear and easier for a human reader to follow, even though the shorter version was slightly more concise. I verified the decision by reviewing the resulting code and rerunning the tests.
- I also used separate chat sessions for different phases of the project so I could focus on implementation, testing, and documentation without mixing concerns.

---

## 4. Testing and Verification

**a. What you tested**

- I tested that high-priority tasks are selected when they fit within the time limit, that tasks are skipped when they do not fit, and that the generated plan includes explanations for both included and skipped tasks.
- These tests are important because they verify the core scheduling behavior that the app depends on.

**b. Confidence**

- I am fairly confident that the current scheduler works correctly for the basic use case because the tests pass and the app displays the generated plan clearly.
- If I had more time, I would test edge cases such as equal-priority tasks, very small time budgets, empty task lists, and tasks that exactly fill the available time.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with connecting the backend scheduler to the user-facing Streamlit app and making the generated plan explain itself in a simple way.

**b. What you would improve**

- In a future iteration, I would improve the scheduler by adding recurring tasks, better time-slot handling, and more detailed reasoning such as preference-based filtering.

**c. Key takeaway**

- One important lesson was that a simple, well-tested design makes it much easier to build and verify an app incrementally.
