package test;

import static org.junit.Assert.*;
import org.junit.Test;

import org.junit.Before;
import org.junit.Ignore;

import java.util.Set;

import org.designwizard.api.DesignWizard;
import org.designwizard.design.ClassNode;
import org.designwizard.design.MethodNode;
import org.designwizard.design.FieldNode;
import org.designwizard.design.PackageNode;

public class DesignTest {
    @Test
    public void testFactoryDoesNotViolateAbstraction() throws Exception {
        // Always instantiate DesignWizard exactly like this
        DesignWizard dw = new DesignWizard("bin");

        // Get the ProductFactory class
        ClassNode productFactory = dw.getClass("com.cnblog.clarck.ProductFactory");

        // Get the createProduct method
        MethodNode createProductMethod = productFactory
                .getDeclaredMethod("createProduct(com.cnblog.clarck.ProductType)");

        // Get the classes that are referenced by the createProduct method
        Set<ClassNode> calleeClasses = createProductMethod.getCalleeClasses();

        // Get the Product class
        ClassNode productClass = dw.getClass("com.cnblog.clarck.Product");

        // Get the concrete product classes
        ClassNode productAClass = dw.getClass("com.cnblog.clarck.ProductA");
        ClassNode productBClass = dw.getClass("com.cnblog.clarck.ProductB");

        // Assert that the createProduct method only references the Product class or its
        // subclasses
        assertTrue(calleeClasses.contains(productClass));
        assertFalse(calleeClasses.contains(productAClass));
        assertFalse(calleeClasses.contains(productBClass));
    }
}
