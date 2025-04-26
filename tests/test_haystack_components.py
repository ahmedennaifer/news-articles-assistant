from src.assistant.components.indexing_components.csv_metadata_extractor import (
    CSVMetadataExtractor,
)


def test_csv_metadat_extractor():
    csv = CSVMetadataExtractor()
    docs = csv.run("data/final.csv")
    assert (
        "Quarterly profits at US media giant TimeWarner jumped 76% to $1.13bn (£600m)"  # first sentence
        in docs[0].content
    )
    assert (
        "It intends to adjust the way it accounts for a deal with German music publisher Bertelsmann's purchase of a stake in AOL Europe, which it had reported as advertising revenue. It will now book the sale of its stake in AOL Europe as a loss on the value of that stake"  # last sentence
        in docs[0].content
    )
    assert docs[0].meta["category"] == "business"
    assert docs[0].meta["title"] == "Ad sales boost Time Warner profit"
    assert len(docs) == 2138
