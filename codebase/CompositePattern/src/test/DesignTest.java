package test;

import static org.junit.Assert.*;
import org.junit.Test;

import org.junit.Before;
import org.junit.Ignore;

import java.util.Set;

import org.designwizard.api.DesignWizard;
import org.designwizard.design.ClassNode;
import org.designwizard.design.Design;
import org.designwizard.design.MethodNode;
import org.designwizard.design.FieldNode;
import org.designwizard.design.PackageNode;
import org.designwizard.exception.InexistentEntityException;
import org.designwizard.design.Modifier;

public class DesignTest {
    @Test
    public void testLeafDoesNotThrowExceptions() throws Exception {
        // Always instantiate DesignWizard exactly like this
        DesignWizard dw = new DesignWizard("bin");

        // Get the Leaf class
        ClassNode leafClass = dw.getClass("com.cnblog.clarck.Leaf");

        // Get the add and remove methods
        MethodNode addMethod = dw.getMethod("com.cnblog.clarck.Leaf.add(com.cnblog.clarck.Component)");
        MethodNode removeMethod = dw.getMethod("com.cnblog.clarck.Leaf.remove(com.cnblog.clarck.Component)");

        // Check that the add method does not throw any exceptions
        Set<ClassNode> addThrownExceptions = addMethod.getThrownExceptions();
        assertTrue("The add method should not throw any exceptions", addThrownExceptions.isEmpty());

        // Check that the remove method does not throw any exceptions
        Set<ClassNode> removeThrownExceptions = removeMethod.getThrownExceptions();
        assertTrue("The remove method should not throw any exceptions", removeThrownExceptions.isEmpty());

        // Check that the add method does not catch any exceptions
        Set<ClassNode> addCatchedExceptions = addMethod.getCatchedExceptions();
        assertTrue("The add method should not catch any exceptions", addCatchedExceptions.isEmpty());

        // Check that the remove method does not catch any exceptions
        Set<ClassNode> removeCatchedExceptions = removeMethod.getCatchedExceptions();
        assertTrue("The remove method should not catch any exceptions", removeCatchedExceptions.isEmpty());
    }

}
