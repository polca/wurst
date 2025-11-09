from brightway_fixtures import test_bw2_database

if test_bw2_database is not None:
    import pytest
    from bw2data.tests import bw2test

    from wurst.brightway import extract_brightway2_databases

    def test_extraction(test_bw2_database):
        expected = [
            {
                "categories": ["stuff", "meals"],
                "classifications": [42],
                "code": "1",
                "comment": "Yep",
                "database": "food",
                "exchanges": [
                    {
                        "name": "dinner",
                        "amount": 0.5,
                        "database": "food",
                        "loc": 0.5,
                        "location": "CH",
                        "product": None,
                        "production volume": 13,
                        "type": "technosphere",
                        "uncertainty type": 0,
                        "unit": "kg",
                    },
                    {
                        "name": "an emission",
                        "amount": 0.05,
                        "categories": ["things"],
                        "input": ("biosphere", "1"),
                        "database": "biosphere",
                        "location": None,
                        "product": "find me!",
                        "production volume": None,
                        "type": "biosphere",
                        "uncertainty type": 4,
                        "unit": "kg",
                    },
                ],
                "location": "CA",
                "name": "lunch",
                "reference product": "stuff",
                "type": "processwithreferenceproduct",
                "unit": "kg",
                "parameters": {"losses_gross_net": 0.01},
                "parameters full": [{"amount": 0.01, "name": "losses_gross_net"}],
            },
            {
                "categories": ["stuff", "meals"],
                "classifications": [],
                "code": "2",
                "comment": "",
                "database": "food",
                "exchanges": [
                    {
                        "name": "lunch",
                        "amount": 0.25,
                        "location": "CA",
                        "product": "stuff",
                        "database": "food",
                        "production volume": None,
                        "type": "technosphere",
                        "uncertainty type": 0,
                        "unit": "kg",
                    },
                    {
                        "name": "another emission",
                        "amount": 0.15,
                        "categories": ["things"],
                        "input": ("biosphere", "2"),
                        "database": "biosphere",
                        "location": None,
                        "product": None,
                        "production volume": None,
                        "type": "biosphere",
                        "uncertainty type": 0,
                        "unit": "kg",
                    },
                ],
                "location": "CH",
                "name": "dinner",
                "reference product": None,
                "type": "processwithreferenceproduct",
                "unit": "kg",
                "parameters": {"rara": 13},
                "parameters full": [
                    {"name": "rara", "amount": 13, "something": "else"}
                ],
            },
        ]

        assert sorted(
            extract_brightway2_databases("food"), key=lambda x: x["code"]
        ) == sorted(expected, key=lambda x: x["code"])

    @bw2test
    def test_extraction_missing_database():
        with pytest.raises(AssertionError):
            assert extract_brightway2_databases("biosphere3")

    def test_extraction_input_formats(test_bw2_database):
        assert extract_brightway2_databases("food")
        assert extract_brightway2_databases(["food"])
        assert extract_brightway2_databases(("food",))
        assert extract_brightway2_databases({"food"})
        with pytest.raises(AssertionError):
            assert extract_brightway2_databases({"food": None})

    def test_extraction_with_properties():
        data = extract_brightway2_databases("food")
        assert all("properties" not in exc for ds in data for exc in ds["exchanges"])
        data = extract_brightway2_databases("food", add_properties=True)
        assert all("properties" in exc for ds in data for exc in ds["exchanges"])

    def test_extraction_with_identifiers():
        data = extract_brightway2_databases("food")
        assert all("properties" not in exc for ds in data for exc in ds["exchanges"])
        data = extract_brightway2_databases("food", add_identifiers=True)
        assert all("id" in ds for ds in data)
        assert all("id" in exc for ds in data for exc in ds["exchanges"])
        assert all("code" in exc for ds in data for exc in ds["exchanges"])

    @bw2test
    def test_extraction_custom_node_type():
        """Test that extract_brightway2_databases correctly extracts custom node types.
        
        This covers the type attribute extraction in extract_database.py line 44.
        """
        from bw2data import Database
        
        # Create a database with a custom node type (not "process" or "emission")
        custom_db = {
            ("custom_test", "1"): {
                "categories": ["custom", "category"],
                "code": "1",
                "classifications": [],
                "comment": "Custom type test",
                "reference product": "custom_product",
                "exchanges": [],
                "location": "GLO",
                "name": "custom_activity",
                "type": "transformation",
                "unit": "kg",
            },
        }
        
        d = Database("custom_test")
        d.write(custom_db)
        
        # Extract the database
        data = extract_brightway2_databases("custom_test")
        
        # Verify the custom type was correctly extracted
        assert len(data) == 1
        assert data[0]["type"] == "transformation"
        assert data[0]["name"] == "custom_activity"
        assert data[0]["code"] == "1"
        assert data[0]["reference product"] == "custom_product"
        assert data[0]["location"] == "GLO"
        assert data[0]["unit"] == "kg"
        assert data[0]["comment"] == "Custom type test"
        assert data[0]["categories"] == ["custom", "category"]

    @bw2test
    def test_write_brightway2_database_with_metadata(test_bw2_database):
        """Test that write_brightway2_database accepts and stores metadata.
        
        This covers the metadata parameter in write_database.py line 22.
        """
        from wurst.brightway import write_brightway2_database
        from bw2data import Database
        
        # Create simple test data that can be written back
        data = [
            {
                "name": "test_activity",
                "unit": "kg",
                "database": "source_db",
                "code": "1",
                "reference product": "test_product",
                "location": "GLO",
                "exchanges": [
                    {
                        "name": "test_activity",
                        "amount": 1,
                        "type": "production",
                        "unit": "kg",
                        "product": "test_product",
                        "location": "GLO",
                        "reference product": "test_product",
                    }
                ],
            }
        ]
        
        # Define custom metadata
        metadata = {
            "description": "Test database with metadata",
            "version": "1.0",
            "author": "test_user"
        }
        
        # Write database with metadata
        write_brightway2_database(data, "test_meta_db", metadata=metadata)
        
        # Verify database was created by trying to retrieve it
        db = Database("test_meta_db")
        
        # Check metadata was stored
        assert "description" in db.metadata
        assert db.metadata["description"] == "Test database with metadata"
        assert db.metadata["version"] == "1.0"
        assert db.metadata["author"] == "test_user"

else:
    pass


# ============================================================================
# MISSING TEST COVERAGE
# ============================================================================
# 
# The following code paths in src/wurst/brightway/ are NOT tested:
#
# EXTRACTION TESTS (extract_database.py):
#
# 1. Write functions completely untested:
#    - write_brightway2_database() - NO TESTS
#    - write_brightway2_array_database() - NO TESTS
#    - WurstImporter.write_database() - NO TESTS
#
# 2. Error cases in write_brightway2_database (write_database.py):
#    - line 49: Database name collision
#    - line 60: Invalid link errors from check_internal_linking()
#    - line 61: Duplicate codes from check_duplicate_codes()
#
# 3. Error cases in extract_brightway2_databases (extract_database.py):
#    - line 161: Wrong database type (non-SQLiteBackend)
#    - line 65: Exchange without amount field (assert failure)
#
# 4. Parameter handling (extract_database.py lines 39-43):
#    - Parameters as list format
#    - Parameters as dict format  
#    - Parameters with extra fields ("parameters full")
#    - Missing parameters handling
#
# 5. Exchange extraction edge cases (extract_database.py lines 50-75):
#    - Missing uncertainty fields
#    - All uncertainty field types (scale, shape, minimum, maximum, pedigree)
#    - Production volume handling
#    - Properties extraction when add_properties=True
#
# 6. External database lookups (extract_database.py lines 119-143):
#    - Cache mechanism for external exchanges
#    - Exchanges from multiple external databases
#    - Failed lookup scenarios
#
# 7. Internal database lookups (extract_database.py lines 96-116):
#    - Missing input info scenarios
#    - Biosphere categories handling
#    - Identifiers handling in exchanges
#
# 8. Edge cases in extraction:
#    - Activities with no exchanges
#    - Exchanges with no matching input activities
#    - Classifications field (empty list vs None)
#    - Categories field (empty list vs None)
#    - Comment field (empty string handling)
#
# 9. IOTable backend (write_database.py lines 65-106):
#     - No tests for array database writing
#     - Key generation for activities
#     - Exchange extraction to separate list
#
# TESTED (NOW COVERED):
# ✓ Metadata parameter in write_brightway2_database (line 22)
#
# ============================================================================
