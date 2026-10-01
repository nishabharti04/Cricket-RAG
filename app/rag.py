import os
import re

from langchain_ollama import ChatOllama

from app.vectorstore import load_vector_store


class CricketRAG:

    def __init__(self):
        self.vector_store = load_vector_store()

        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0,
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434"
            )
        )

    # =========================================================
    # WINNER
    # =========================================================
    def extract_winner(self, context: str):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            context
        )

        patterns = [
            r'^(.+?)\s+won the tournament',
            r'^(.+?)\s+won the .*?World Cup',
            r'^(.+?)\s+won the .*?Cup'
        ]

        for sentence in sentences:

            sentence = sentence.strip()

            for pattern in patterns:

                match = re.search(
                    pattern,
                    sentence,
                    re.IGNORECASE
                )

                if match:
                    return match.group(1).strip()

        return None

    # =========================================================
    # DEFEATED TEAM
    # =========================================================
    def extract_defeated_team(self, context: str):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            context
        )

        patterns = [
            r'by defeating\s+(.+?)\s+in the final',
            r'defeating\s+(.+?)\s+in the final'
        ]

        for sentence in sentences:

            for pattern in patterns:

                match = re.search(
                    pattern,
                    sentence,
                    re.IGNORECASE
                )

                if match:
                    return match.group(1).strip()

        return None

    # =========================================================
    # SCORER BY RUNS
    # =========================================================
    def extract_scorer(self, context: str, question: str):

        # Find number of runs in question
        run_match = re.search(
            r'\b(\d+)\s+runs?\b',
            question,
            re.IGNORECASE
        )

        if not run_match:
            return None

        runs = run_match.group(1)

        sentences = re.split(
            r'(?<=[.!?])\s+',
            context
        )

        # Example:
        # Virat Kohli scored 765 runs during the tournament.
        pattern = rf'(.+?)\s+scored\s+{runs}\s+runs?'

        for sentence in sentences:

            match = re.search(
                pattern,
                sentence,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None

    # =========================================================
    # VENUE
    # =========================================================
    def extract_venue(self, context: str):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            context
        )

        for sentence in sentences:

            match = re.search(
                r'\bplayed\s+at\s+(.+?)\s+in\s+',
                sentence,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

            match = re.search(
                r'\bplayed\s+at\s+([^,.]+)',
                sentence,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None

    # =========================================================
    # HOST LOCATION
    # =========================================================
    def extract_host_location(self, context: str):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            context
        )

        for sentence in sentences:

            match = re.search(
                r'\bwas\s+held\s+in\s+(.+?)(?:\.|,|$)',
                sentence,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None

    # =========================================================
    # YEAR
    # =========================================================
    def extract_year(self, context: str):

        years = re.findall(
            r'\b(?:18|19|20)\d{2}\b',
            context
        )

        if years:
            return years[0]

        return None

    # =========================================================
    # GENERAL FALLBACK
    # =========================================================
    def extractive_fallback(self, question: str, context: str):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            context
        )

        question_words = set(
            word.lower()
            for word in re.findall(
                r'\b[a-zA-Z0-9]+\b',
                question
            )
        )

        best_sentence = ""
        best_score = 0

        for sentence in sentences:

            sentence_words = set(
                word.lower()
                for word in re.findall(
                    r'\b[a-zA-Z0-9]+\b',
                    sentence
                )
            )

            score = len(
                question_words.intersection(
                    sentence_words
                )
            )

            if score > best_score:

                best_score = score
                best_sentence = sentence.strip()

        if best_sentence:
            return best_sentence

        return (
            "I don't have that information in my "
            "cricket knowledge base."
        )

    # =========================================================
    # LLM
    # =========================================================
    def ask_llm(self, question: str, context: str):

        prompt = f"""
Answer the user's question using ONLY the context.

Return ONLY the answer to the question.
Do not provide a numbered list.
Do not explain your reasoning.
Do not answer additional questions.
Do not add unrelated facts.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()

    # =========================================================
    # MAIN RAG
    # =========================================================
    def ask(self, question: str):

        # -----------------------------------------------------
        # RETRIEVAL
        # -----------------------------------------------------

        results = self.vector_store.similarity_search_with_score(
            question,
            k=1
        )

        if not results:

            return {
                "question": question,
                "answer": (
                    "I don't have that information in my "
                    "cricket knowledge base."
                ),
                "sources": [],
                "method": "no_retrieval"
            }

        docs = [doc for doc, score in results]

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        q = question.lower()

        # -----------------------------------------------------
        # 1. SCORER QUESTIONS
        # -----------------------------------------------------

        if (
            "who scored" in q
            and re.search(r'\b\d+\s+runs?\b', q)
        ):

            extracted = self.extract_scorer(
                context,
                question
            )

            if extracted:

                answer = extracted
                method = "context_extraction"

            else:

                answer = self.ask_llm(
                    question,
                    context
                )

                method = "llm"

        # -----------------------------------------------------
        # 2. DEFEATED TEAM
        # -----------------------------------------------------

        elif (
            "who did" in q
            and "defeat" in q
        ):

            extracted = self.extract_defeated_team(context)

            if extracted:

                answer = extracted
                method = "context_extraction"

            else:

                answer = self.ask_llm(
                    question,
                    context
                )

                method = "llm"

        # -----------------------------------------------------
        # 3. WINNER
        # -----------------------------------------------------

        elif (
            q.startswith("who won")
            or q.startswith("which team won")
            or "who was the winner" in q
        ):

            extracted = self.extract_winner(context)

            if extracted:

                answer = extracted
                method = "context_extraction"

            else:

                answer = self.ask_llm(
                    question,
                    context
                )

                method = "llm"

        # -----------------------------------------------------
        # 4. WHERE
        # -----------------------------------------------------

        elif q.startswith("where"):

            if (
                "held" in q
                or "hosted" in q
            ):

                extracted = self.extract_host_location(context)

            else:

                extracted = self.extract_venue(context)

            if extracted:

                answer = extracted
                method = "context_extraction"

            else:

                answer = self.ask_llm(
                    question,
                    context
                )

                method = "llm"

        # -----------------------------------------------------
        # 5. WHEN
        # -----------------------------------------------------

        elif q.startswith("when"):

            extracted = self.extract_year(context)

            if extracted:

                answer = extracted
                method = "context_extraction"

            else:

                answer = self.ask_llm(
                    question,
                    context
                )

                method = "llm"

        # -----------------------------------------------------
        # 6. OTHER QUESTIONS
        # -----------------------------------------------------

        else:

            answer = self.ask_llm(
                question,
                context
            )

            refusal_phrases = [
                "i don't have that information",
                "i do not have that information",
                "information is not available",
                "cannot answer",
                "can't answer",
                "unable to answer"
            ]

            if any(
                phrase in answer.lower()
                for phrase in refusal_phrases
            ):

                answer = self.extractive_fallback(
                    question,
                    context
                )

                method = "extractive_fallback"

            else:

                method = "llm"

        # -----------------------------------------------------
        # SOURCES
        # -----------------------------------------------------

        sources = []

        for doc, score in results:

            sources.append({
                "source": doc.metadata.get(
                    "source",
                    "unknown"
                ),
                "distance_score": round(
                    float(score),
                    4
                ),
                "content": doc.page_content[:400]
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "method": method
        }