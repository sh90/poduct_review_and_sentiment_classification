import streamlit as st

from profiles import load_user_profile, save_user_profile, bookmark, add_note
from agent import ask_agent, extract_code_from_answer
from unit_tests import generate_unit_tests, run_unit_tests, suggest_missing_test_cases, regenerate_tests_with_feedback, \
    refine_code_with_test_failures
from memory import ingest_codebase

# --- User Login ---
if "user" not in st.session_state:
    st.session_state["user"] = None

if not st.session_state["user"]:
    username = st.text_input("Enter your username to log in:")
    if st.button("Log in"):
        profile = load_user_profile(username)
        save_user_profile(profile)
        st.session_state["user"] = profile
        st.session_state["history"] = []
        st.success(f"Logged in as {username}")

if st.session_state["user"]:
    profile = st.session_state["user"]
    st.sidebar.write(f"Hello, {profile['username']}!")

    # --- Profile Preferences ---
    with st.sidebar.expander("Preferences"):
        framework = st.selectbox("Test Framework", ["unittest", "pytest"], index=0 if profile["preferences"]["test_framework"] == "unittest" else 1)
        indent = st.selectbox("Indentation Style", ["    ", "\t"], index=0 if profile["preferences"]["indent_style"] == "    " else 1)
        docstring_fmt = st.selectbox("Docstring Format", ["google", "numpy", "sphinx"], index=["google", "numpy", "sphinx"].index(profile["preferences"]["docstring_format"]))
        if st.button("Save Preferences"):
            profile["preferences"].update({
                "test_framework": framework,
                "indent_style": indent,
                "docstring_format": docstring_fmt
            })
            save_user_profile(profile)
            st.success("Preferences updated!")

    # --- Ingest Project ---
    st.sidebar.header("🔄 Ingest Project")
    code_root = st.sidebar.text_input("Project root folder", value="./example_project")
    if st.sidebar.button("Ingest Codebase"):
        ingest_codebase(code_root)
        st.sidebar.success("Codebase ingested and indexed!")

    st.title("💻 AI Coding Assistant (with Unit Tests Generation)")
    user_query = st.text_area("Your question or code edit request:", height=100)

    # --- Main Assistant Button ---
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            history = st.session_state.get("history", [])
            answer, retrieved = ask_agent(user_query, history)
            st.session_state["history"].append((user_query, answer))
            code, explanation = extract_code_from_answer(answer)
            st.session_state["latest_query"] = user_query
            st.session_state["latest_answer"] = answer
            st.markdown("**Assistant:**")
            if explanation.strip():
                st.write(explanation)
            if code:
                st.markdown("**Proposed Code Edit:**")
                st.code(code, language="python")
                st.session_state["last_generated_code"] = code
            else:
                st.write(answer)
            with st.expander("🔍 Context Used"):
                for i, (chunk, cid) in enumerate(retrieved):
                    st.markdown(f"**Context {i + 1}** (`{cid}`):\n```python\n{chunk}\n```")

    # --- Bookmark Button (ALWAYS VISIBLE IF LATEST Q&A EXISTS) ---
    if st.session_state.get("latest_answer"):
        if st.button("Bookmark this answer"):
            bookmark(profile, st.session_state["latest_query"], st.session_state["latest_answer"])
            st.session_state["user"] = load_user_profile(profile["username"])
            st.success("Bookmarked!")

    # In your Unit Test Helper section, pre-fill with last generated code if available:

    # --- Unit Testing Workflow ---
    st.markdown("---\n## ====== Unit Test Helper ====== ")
    code_input = st.text_area(
        "Paste function/class to generate tests for:",
        value=st.session_state.get("last_generated_code", ""),
        height=120,
        key="testcode"
    )
    if st.button("Generate Unit Tests"):
        if code_input.strip():
            test_code = generate_unit_tests(code_input)
            st.session_state["last_test_code"] = test_code
            st.markdown("**Generated Unit Tests:**")
            st.code(test_code, language="python")

    if "last_test_code" in st.session_state and st.button("Run Generated Tests"):
        result = run_unit_tests(st.session_state["last_test_code"])
        st.markdown("**Test Results:**")
        st.code(result)

        # Suggest missing cases
        suggestion = suggest_missing_test_cases(code_input, st.session_state["last_test_code"])
        st.session_state["test_suggestions"] = suggestion
        st.markdown("**Suggestions for Additional Test Cases:**")
        st.write(suggestion)

    # --- ITERATIVE REFINEMENT SECTION ---
    if "test_suggestions" in st.session_state:
        suggestion_text = st.text_area(
            "Refine/add suggestions and submit for improved tests:",
            value=st.session_state["test_suggestions"],
            height=100,
            key="suggestion_text"
        )
        if st.button("Refine and Regenerate Unit Tests"):
            improved_tests = regenerate_tests_with_feedback(
                code_input,
                st.session_state["last_test_code"],
                suggestion_text
            )
            st.session_state["last_test_code"] = improved_tests
            st.markdown("**Improved/Refined Unit Tests:**")
            st.code(improved_tests, language="python")
        # Optionally, immediately offer to run the new tests:
        # Always display "Run Improved Tests" if last_test_code exists
        if st.session_state.get("last_test_code"):
                if st.button("Run Improved Tests"):
                    result = run_unit_tests(st.session_state["last_test_code"])
                    st.session_state["last_test_result"] = result
                    st.markdown("**Improved Test Results:**")
                    st.code(result)

    # We store last function, tests, and results in session_state
    code_to_fix = code_input
    tests_used = st.session_state.get("last_test_code", "")
    last_results = st.session_state.get("last_test_result", "")

    if st.button("Refine Original Code Based on Failing Tests"):
        print("=======Code to be fixed======")
        print(code_to_fix)
        print("=======Tests Used=======")
        print(tests_used)
        print("=======Last results=====")
        print(last_results)
        print("inside")
        check = code_to_fix and tests_used and last_results
        print("Value of check",check)
        if code_to_fix and tests_used and last_results:
            fixed_code = refine_code_with_test_failures(code_to_fix, tests_used, last_results)
            st.session_state["last_generated_code"] = fixed_code
            st.markdown("**Refined/Corrected Function Code:**")
            st.code(fixed_code, language="python")


    # --- Bookmarks/Notes ---
    st.markdown("---\n## 📑 Bookmarks")
    for bm in reversed(profile.get("bookmarks", [])):
        st.markdown(f"**[{bm['timestamp']}]**  \nQuery: `{bm['query']}`  \nAnswer: {bm['answer'][:500]}...")

    st.markdown("---\n## 🗒️ Personal Notes")
    note_text = st.text_area("Add a note (for yourself):", key="note")
    if st.button("Save Note"):
        add_note(profile, note_text)
        st.success("Note saved!")
    for note in reversed(profile.get("notes", [])):
        st.markdown(f"**[{note['timestamp']}]**  \n{note['note']}")

    # --- Chat History ---
    if st.session_state.get("history"):
        st.markdown("---\n**Chat History:**")
        for q, a in st.session_state["history"]:
            st.markdown(f"**You:** {q}\n\n**Assistant:** {a}")

else:
    st.warning("Please log in to continue.")

