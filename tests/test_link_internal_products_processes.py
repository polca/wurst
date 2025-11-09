"""Unit tests for link_internal_products_processes function."""
import pytest

from bw2data import labels
from wurst.brightway.write_database import link_internal_products_processes


class TestLinkInternalProductsProcesses:
    """Test suite for link_internal_products_processes function."""

    def test_basic_technosphere_linking(self):
        """Test basic linking of technosphere exchanges to products."""
        # Create a product node using actual Brightway product type
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        product = {
            "database": "test_db",
            "code": "prod_1",
            "name": "test_product",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        # Create a process with an unlinked technosphere exchange
        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [product, process]
        count = link_internal_products_processes(data)

        assert count == 1
        assert process["exchanges"][0]["input"] == ("test_db", "prod_1")

    def test_basic_biosphere_linking(self):
        """Test basic linking of biosphere exchanges to flows."""
        # Create a biosphere flow using actual Brightway flow type
        flow_type = labels.biosphere_node_default
        process_type = labels.process_node_default
        
        flow = {
            "database": "biosphere",
            "code": "flow_1",
            "name": "CO2",
            "unit": "kg",
            "categories": ("air",),
            "type": flow_type,
        }

        # Create a process with an unlinked biosphere exchange
        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "CO2",
                    "unit": "kg",
                    "categories": ("air",),
                    "type": "biosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [flow, process]
        count = link_internal_products_processes(data)

        assert count == 1
        assert process["exchanges"][0]["input"] == ("biosphere", "flow_1")

    def test_already_linked_exchanges_skipped(self):
        """Test that exchanges with existing input are skipped."""
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        product = {
            "database": "test_db",
            "code": "prod_1",
            "name": "test_product",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                    "input": ("other_db", "other_code"),  # Already linked
                }
            ],
        }

        data = [product, process]
        count = link_internal_products_processes(data)

        assert count == 0
        assert process["exchanges"][0]["input"] == ("other_db", "other_code")

    def test_unlinked_exchanges_remain_unlinked(self):
        """Test that exchanges without matching products/flows remain unlinked."""
        process_type = labels.process_node_default
        
        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "nonexistent_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [process]
        count = link_internal_products_processes(data)

        assert count == 0
        assert "input" not in process["exchanges"][0]

    def test_custom_biosphere_fields(self):
        """Test linking with custom biosphere field list."""
        flow_type = labels.biosphere_node_default
        process_type = labels.process_node_default
        
        flow = {
            "database": "biosphere",
            "code": "flow_1",
            "name": "CO2",
            "unit": "kg",
            "categories": ("air",),
            "type": flow_type,
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "CO2",
                    "unit": "kg",
                    "categories": ("air",),
                    "type": "biosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [flow, process]
        # Use custom fields that match
        count = link_internal_products_processes(
            data, biosphere_fields=["name", "unit", "categories"]
        )

        assert count == 1
        assert process["exchanges"][0]["input"] == ("biosphere", "flow_1")

    def test_custom_technosphere_fields(self):
        """Test linking with custom technosphere field list."""
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        product = {
            "database": "test_db",
            "code": "prod_1",
            "name": "test_product",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [product, process]
        # Use custom fields that match
        count = link_internal_products_processes(
            data, technosphere_fields=["name", "unit", "location"]
        )

        assert count == 1
        assert process["exchanges"][0]["input"] == ("test_db", "prod_1")

    def test_multiple_exchanges_same_process(self):
        """Test linking multiple exchanges in the same process."""
        product_type = labels.product_node_default
        flow_type = labels.biosphere_node_default
        process_type = labels.process_node_default
        
        product1 = {
            "database": "test_db",
            "code": "prod_1",
            "name": "product1",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        product2 = {
            "database": "test_db",
            "code": "prod_2",
            "name": "product2",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        flow = {
            "database": "biosphere",
            "code": "flow_1",
            "name": "CO2",
            "unit": "kg",
            "categories": ("air",),
            "type": flow_type,
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "product1",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                },
                {
                    "name": "product2",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 2.0,
                },
                {
                    "name": "CO2",
                    "unit": "kg",
                    "categories": ("air",),
                    "type": "biosphere",
                    "amount": 3.0,
                },
            ],
        }

        data = [product1, product2, flow, process]
        count = link_internal_products_processes(data)

        assert count == 3
        assert process["exchanges"][0]["input"] == ("test_db", "prod_1")
        assert process["exchanges"][1]["input"] == ("test_db", "prod_2")
        assert process["exchanges"][2]["input"] == ("biosphere", "flow_1")

    def test_multiple_processes(self):
        """Test linking exchanges across multiple processes."""
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        product = {
            "database": "test_db",
            "code": "prod_1",
            "name": "test_product",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        process1 = {
            "database": "test_db",
            "code": "proc_1",
            "name": "process1",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                }
            ],
        }

        process2 = {
            "database": "test_db",
            "code": "proc_2",
            "name": "process2",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 2.0,
                }
            ],
        }

        data = [product, process1, process2]
        count = link_internal_products_processes(data)

        assert count == 2
        assert process1["exchanges"][0]["input"] == ("test_db", "prod_1")
        assert process2["exchanges"][0]["input"] == ("test_db", "prod_1")

    def test_return_count(self):
        """Test that the function returns the correct count of linked edges."""
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        products = [
            {
                "database": "test_db",
                "code": f"prod_{i}",
                "name": f"product{i}",
                "unit": "kg",
                "location": "GLO",
                "type": product_type,
            }
            for i in range(3)
        ]

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": f"product{i}",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": float(i),
                }
                for i in range(3)
            ],
        }

        data = products + [process]
        count = link_internal_products_processes(data)

        assert count == 3

    def test_natural_resource_flow_type(self):
        """Test that natural resource flows are recognized."""
        process_type = labels.process_node_default
        
        flow = {
            "database": "biosphere",
            "code": "flow_1",
            "name": "water",
            "unit": "m3",
            "categories": ("resource",),
            "type": "natural resource",
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "water",
                    "unit": "m3",
                    "categories": ("resource",),
                    "type": "biosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [flow, process]
        count = link_internal_products_processes(data)

        assert count == 1
        assert process["exchanges"][0]["input"] == ("biosphere", "flow_1")

    def test_resource_flow_type(self):
        """Test that resource flows are recognized."""
        process_type = labels.process_node_default
        
        flow = {
            "database": "biosphere",
            "code": "flow_1",
            "name": "iron",
            "unit": "kg",
            "categories": ("resource",),
            "type": "resource",
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "iron",
                    "unit": "kg",
                    "categories": ("resource",),
                    "type": "biosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [flow, process]
        count = link_internal_products_processes(data)

        assert count == 1
        assert process["exchanges"][0]["input"] == ("biosphere", "flow_1")

    def test_social_flow_type(self):
        """Test that social flows are recognized."""
        process_type = labels.process_node_default
        
        flow = {
            "database": "biosphere",
            "code": "flow_1",
            "name": "work",
            "unit": "hours",
            "categories": ("social",),
            "type": "social",
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "work",
                    "unit": "hours",
                    "categories": ("social",),
                    "type": "biosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [flow, process]
        count = link_internal_products_processes(data)

        assert count == 1
        assert process["exchanges"][0]["input"] == ("biosphere", "flow_1")

    def test_mixed_linked_and_unlinked(self):
        """Test process with mix of linked and unlinked exchanges."""
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        product = {
            "database": "test_db",
            "code": "prod_1",
            "name": "test_product",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 1.0,
                },
                {
                    "name": "nonexistent",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 2.0,
                },
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "GLO",
                    "type": "technosphere",
                    "amount": 3.0,
                    "input": ("already", "linked"),  # Already linked
                },
            ],
        }

        data = [product, process]
        count = link_internal_products_processes(data)

        assert count == 1
        assert process["exchanges"][0]["input"] == ("test_db", "prod_1")
        assert "input" not in process["exchanges"][1]
        assert process["exchanges"][2]["input"] == ("already", "linked")

    def test_empty_exchanges_list(self):
        """Test process with empty exchanges list."""
        process_type = labels.process_node_default
        
        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [],
        }

        data = [process]
        count = link_internal_products_processes(data)

        assert count == 0

    def test_missing_exchanges_key(self):
        """Test process without exchanges key.
        
        Note: The function accesses ds["exchanges"] directly, so this will raise KeyError.
        This test documents the current behavior - processes must have an exchanges key.
        """
        process_type = labels.process_node_default
        
        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
        }

        data = [process]
        # The function accesses ds["exchanges"] directly, so this will raise KeyError
        with pytest.raises(KeyError):
            link_internal_products_processes(data)

    def test_field_mismatch_no_linking(self):
        """Test that mismatched fields prevent linking."""
        product_type = labels.product_node_default
        process_type = labels.process_node_default
        
        product = {
            "database": "test_db",
            "code": "prod_1",
            "name": "test_product",
            "unit": "kg",
            "location": "GLO",
            "type": product_type,
        }

        process = {
            "database": "test_db",
            "code": "proc_1",
            "name": "test_process",
            "type": process_type,
            "exchanges": [
                {
                    "name": "test_product",
                    "unit": "kg",
                    "location": "CH",  # Different location
                    "type": "technosphere",
                    "amount": 1.0,
                }
            ],
        }

        data = [product, process]
        count = link_internal_products_processes(data)

        assert count == 0
        assert "input" not in process["exchanges"][0]

