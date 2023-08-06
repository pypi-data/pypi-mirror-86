import torch
from flair.embeddings import DocumentPoolEmbeddings, WordEmbeddings, Embeddings, TransformerDocumentEmbeddings
from flair.data import Sentence
from typing import List
from nlp_gym.envs.question_answering.observation import Observation, ObservationFeaturizer


class InformedFeaturizer(ObservationFeaturizer):
    def __init__(self, device: str = "cpu"):
        self.device = device
        self._setup_device()
        self.doc_embeddings = DocumentPoolEmbeddings([WordEmbeddings("en")])

    def init_on_reset(self, question: str, facts: List[str]):
        pass

    def featurize(self, observation: Observation) -> torch.Tensor:
        sim_scores = [self._get_sim(observation.get_question(), observation.get_choice()),
                      self._get_sim(".".join(observation.get_facts()), observation.get_choice())]
        sim_scores = torch.tensor(sim_scores)
        return sim_scores

    def get_observation_dim(self):
        return 2

    def _get_sentence_embedding(self, text: str) -> torch.Tensor:
        text = "..." if len(text) == 0 else text
        sent = Sentence(text)
        self.doc_embeddings.embed(sent)
        if len(sent) > 1:
            embedding = torch.tensor(sent.embedding.cpu().numpy()).reshape(1, -1)
        else:
            embedding = torch.tensor(sent[0].embedding.cpu().numpy()).reshape(1, -1)
        return embedding

    def _setup_device(self):
        import flair, torch
        flair.device = torch.device(self.device)

    def _get_sim(self, query: str, choice_text: str):
        sim = torch.nn.CosineSimilarity(dim=1)(self._get_sentence_embedding(query),
                                               self._get_sentence_embedding(choice_text))
        return sim


class SimpleFeaturizer(ObservationFeaturizer):
    def __init__(self, doc_embeddings: Embeddings = None,
                 device: str = "cpu"):
        self.device = device
        self._setup_device()
        self.doc_embeddings = doc_embeddings if doc_embeddings else DocumentPoolEmbeddings([WordEmbeddings("en")])

    @classmethod
    def from_fasttext(cls) -> 'SimpleFeaturizer':
        return cls(DocumentPoolEmbeddings([WordEmbeddings("en")]))

    @classmethod
    def from_transformers(cls) -> 'SimpleFeaturizer':
        return cls(TransformerDocumentEmbeddings())

    def init_on_reset(self, question: str, facts: List[str]):
        pass

    def featurize(self, observation: Observation) -> torch.Tensor:
        question_embedding = self._get_sentence_embedding(observation.get_question())
        fact_embedding = self._get_sentence_embedding(".".join(observation.get_facts()))
        choice_embedding = self._get_sentence_embedding(observation.get_choice())
        combined = torch.cat((question_embedding, fact_embedding, choice_embedding), dim=1).flatten()
        return combined

    def get_observation_dim(self):
        embedding = self._get_sentence_embedding("A random sentence to infer dim")
        return embedding.shape[1] * 3  # for question, fact and choice

    def _setup_device(self):
        import flair, torch
        flair.device = torch.device(self.device)

    def _get_sentence_embedding(self, text: str) -> torch.Tensor:
        text = "..." if len(text) == 0 else text
        sent = Sentence(text)
        self.doc_embeddings.embed(sent)
        if len(sent) >= 1:
            embedding = torch.tensor(sent.embedding.cpu().detach().numpy()).reshape(1, -1)
        else:
            embedding = torch.tensor(sent[0].embedding.cpu().detach().numpy()).reshape(1, -1)
        sent.clear_embeddings()
        return embedding
